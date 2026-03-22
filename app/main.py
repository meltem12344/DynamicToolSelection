import os
import importlib
import inspect
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükle
load_dotenv()

from app.tools.tool_registry import ToolRegistry
from app.search.embedding_search import AdvancedToolSearcher
from app.agent.main_agent import DynamicAgent
from app.tools.base_tool import BaseTool

def auto_discover_tools(registry: ToolRegistry):
    """
    [SIFIR DOKUNUŞ MİMARİSİ]
    tools/implementations klasöründeki tüm Python dosyalarını tarar.
    İçindeki araç sınıflarını (BaseTool'dan türetilmiş olanları) bulur
    ve koda hiçbir manuel 'import' eklemeye gerek kalmadan sisteme otomatik kaydeder.
    """
    print("\n[Auto-Discovery] Araçlar otomatik olarak taranıyor...")
    
    # implementations klasörünün yolunu bul
    current_dir = os.path.dirname(__file__)
    tools_dir = os.path.join(current_dir, "tools", "implementations")
    
    # Klasördeki tüm dosyaları dön
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            # Dosya adından modül yolunu oluştur (Örn: app.tools.implementations.weather_tool)
            module_name = f"app.tools.implementations.{filename[:-3]}"
            
            # Modülü dinamik olarak içeri aktar (sihir burada başlıyor)
            module = importlib.import_module(module_name)
            
            # Modülün içindeki tüm sınıfları (class) tara
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Eğer sınıf BaseTool'dan miras almışsa ve BaseTool'un kendisi değilse, bu bir araçtır!
                if issubclass(obj, BaseTool) and obj is not BaseTool:
                    tool_instance = obj()
                    registry.register(tool_instance)
                    print(f"  -> '{name}' başarıyla keşfedildi ve veritabanına eklendi.")

def setup_system() -> DynamicAgent:
    print("Sistem Başlatılıyor...\n")
    
    registry = ToolRegistry()
    
    # ARTIK ARAÇLARI ELLE KAYDETMİYORUZ! OTONOM KEŞİF DEVREDE!
    auto_discover_tools(registry)
    
    searcher = AdvancedToolSearcher(registry)
    agent = DynamicAgent(registry, searcher)
    
    return agent

if __name__ == "__main__":
    my_agent = setup_system()
    
    print("\n" + "="*50)
    print(" 🤖 UtaiSOFT AI Agent Başarıyla Başlatıldı!")
    print(" Sistemden çıkmak için 'çıkış', 'exit' veya 'quit' yazabilirsiniz.")
    print("="*50 + "\n")
    
    # İnteraktif Sohbet Döngüsü (Case Study Beklentisi)
    while True:
        try:
            # Kullanıcıdan anlık girdi al
            kullanici_girdisi = input("\nSen: ")
            
            # Çıkış komutları kontrolü
            if kullanici_girdisi.lower() in ['çıkış', 'exit', 'quit']:
                print("\n[Sistem]: Görüşmek üzere! Sistem kapatılıyor...")
                break
                
            # Boş enter'a basılırsa atla
            if not kullanici_girdisi.strip():
                continue
                
            # Ajanı kullanıcının girdiği soruyla çalıştır
            my_agent.run(kullanici_girdisi)
            
        except KeyboardInterrupt:
            # CTRL+C ile çıkışı zarifçe yakala
            print("\n[Sistem]: Program zorla kapatıldı. Görüşmek üzere!")
            break
        except Exception as e:
            # Beklenmedik bir hatada programın çökmesini engelle
            print(f"\n[Hata]: Beklenmeyen bir sorun oluştu: {e}")