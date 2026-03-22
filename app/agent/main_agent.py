import json
import os
from openai import OpenAI
from app.search.embedding_search import AdvancedToolSearcher
from app.tools.tool_registry import ToolRegistry

class DynamicAgent:
    """
    Sıfır bilgi (Zero-Knowledge) ile başlayan, ihtiyacı olan araçları
    dinamik olarak arama motorundan (ToolSearcher) çekip kullanan ana ajan.
    """
    def __init__(self, registry: ToolRegistry, searcher: AdvancedToolSearcher):
        self.registry = registry
        self.searcher = searcher
        # API anahtarını ortam değişkenlerinden (.env) çekiyoruz
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Ajanın temel kişiliği (Hangi araçlar olduğunu BİLMİYOR)
        self.system_prompt = """Sen akıllı ve otonom bir asistansın.
Sistemde hangi araçların olduğunu başlangıçta bilmiyorsun. Sana her istekte,
kullanıcının sorusuna en uygun olabilecek araçların kullanım kılavuzları (şemaları) dinamik olarak verilecek.
Eğer verilen araçlar soruyu çözmek için uygunsa onları kullan. Uygun değilse veya araç verilmediyse,
kendi bilginle cevap ver veya 'Bu işlem için uygun bir araca sahip değilim' de. Halüsinasyon görme."""

    def run(self, user_prompt: str):
        print(f"\n[{'-'*10} YENİ GÖREV {'-'*10}]")
        print(f"Kullanıcı: {user_prompt}")
        
        # ADIM 1: DİNAMİK ARAÇ ARAMA (Zero-Knowledge Kısıtının Çözümü)
        # Sadece bu göreve uygun, False-Positive testini geçmiş araçların şemalarını al.
        relevant_schemas = self.searcher.search(user_prompt, top_k=2)
        
        # Eğer uygun araç bulunamadıysa, LLM'e boş bir araç listesi gidecek.
        tools_for_llm = []
        if relevant_schemas:
            # Pydantic şemalarını OpenAI'ın beklediği formata (Dict) çevir
            for schema in relevant_schemas:
                # Aracı bulduk, şimdi kayıt defterinden asıl obje halini alıyoruz
                tool_obj = self.registry.get_tool(schema.name)
                tools_for_llm.append(tool_obj.get_tool_definition())
                print(f"[Main Agent] LLM'e '{schema.name}' aracının yetkisi verildi.")
        else:
            print("[Main Agent] Bu görev için uygun bir araç bulunamadı. LLM aracı olmadan cevap verecek.")

        # ADIM 2: LLM İLE İLETİŞİM (İlk Çağrı)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        print("\n[Main Agent] LLM Düşünüyor...")
        # Eğer tool_for_llm boşsa, tools parametresini göndermiyoruz (hata vermemesi için)
        api_kwargs = {
            "model": "gpt-4o-mini", # Hızlı ve ucuz olduğu için prototiplerde idealdir
            "messages": messages
        }
        if tools_for_llm:
            api_kwargs["tools"] = tools_for_llm
            api_kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**api_kwargs)
        response_message = response.choices[0].message

        # ADIM 3: ARAÇ ÇAĞRISI KONTROLÜ VE ÇALIŞTIRMA (Execution)
        # LLM bir araç kullanmaya karar verdi mi?
        if response_message.tool_calls:
            messages.append(response_message) # LLM'in araç kullanma isteğini mesaja ekle
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                # LLM'in ürettiği parametreleri JSON'dan Python sözlüğüne (Dict) çevir
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"[Aksiyon] LLM '{function_name}' aracını şu parametrelerle çağırdı: {function_args}")
                
                # Aracı kayıt defterinden bul ve çalıştır!
                tool_to_run = self.registry.get_tool(function_name)
                function_result = tool_to_run.execute(**function_args)
                
                print(f"[Gözlem] Araç Çıktısı: {function_result}")
                
                # ADIM 4: SONUCU LLM'E GERİ VERME
                # Aracın ürettiği sonucu LLM'e verip nihai bir cevap oluşturmasını istiyoruz
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_result),
                })
                
            print("\n[Main Agent] Araç sonuçları değerlendiriliyor...")
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            print(f"\n[Nihai Cevap] Asistan: {final_response.choices[0].message.content}")
        else:
            # LLM araç kullanmaya gerek duymadıysa doğrudan cevabı yazdır
            print(f"\n[Nihai Cevap] Asistan: {response_message.content}")