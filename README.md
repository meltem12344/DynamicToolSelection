# Dynamic Tool Selection and Agent Architecture
Case study kapsamında agent çalışması.

Bu proje, LLM tabanlı ajanların geniş araç havuzları içerisinden doğru aracı seçmesini sağlayan modüler bir tool routing mimarisidir. Sistem, semantic search ve cross-encoder tabanlı re-ranking tekniklerini birleştirerek kullanıcı niyetine en uygun aracı belirler ve false-positive riskini azaltır.

## 🏗️ Mimari Bileşenler

Sistem, vaka çalışmasında istenen kısıtlara %100 uyumlu olarak 3 ana modüle ayrılmıştır:

1. **Main Agent (`app/agent/main_agent.py`):** Sistemin merkezidir. "Sıfır Bilgi (Zero-Knowledge)" prensibiyle başlar. System prompt'una hiçbir aracın şeması (schema) veya adı gömülmemiştir (Hardcoded değildir). İhtiyacı olan araçları her istekte dinamik olarak arama motorundan talep eder.
2. **Tool Registry & Auto-Discovery (`app/tools/tool_registry.py` & `main.py`):**
   Sistemdeki araçların meta verilerini tutan dinamik yapıdır. **Open-Closed Prensibi** gereği sisteme yeni bir araç eklendiğinde hiçbir çekirdek koda dokunulmaz. `importlib` kullanılarak yazılan "Auto-Discovery" mekanizması, klasöre eklenen yeni `.py` araç dosyalarını otomatik olarak keşfeder ve vektör veritabanına kaydeder.
3. **Advanced Tool Searcher (`app/search/embedding_search.py`):**
   Ajan (LLM) ile Tool Registry arasındaki yapay zeka tabanlı akıllı filtredir. 100+ araçlık devasa senaryolarda alakasız araçların (False-Positive) ajana gidip token maliyeti yaratmasını engellemek için İki Aşamalı Kurumsal Reranking (Two-Stage Enterprise Reranking) mimarisi kullanır.
   İlk aşamada (Retrieval), paraphrase-multilingual-MiniLM modeli ile çok dilli anlamsal (Semantic) havuz taraması yapılır.
   İkinci aşamada (Re-Ranking), Çekilen aday araçlar, bir Cross-Encoder (ms-marco) modeli tarafından kullanıcının cümlesiyle bağlamsal olarak yan yana okunur, kesin bir uyumluluk skoruna dönüştürülür ve LLM'e sadece en mantıklı araçlar sunulur.

## 🔹Semantic Tool Selection ve False-Positive Azaltma Yaklaşımı


Bu projede, kullanıcı sorgusuna en uygun aracın seçilmesi için iki aşamalı bir semantik arama mimarisi geliştirilmiştir. İlk aşamada, tüm araçlar zenginleştirilmiş açıklamalarıyla birlikte vektör veritabanına (ChromaDB) gömülmüş ve çok dilli bir embedding modeli kullanılarak sorguya en yakın aday araçlar (top-k retrieval) belirlenmiştir. Bu aşamada yalnızca kısa açıklamalar değil; araç yetenekleri, anahtar kelimeler, kullanım örnekleri ve negatif örnekler de embedding metnine dahil edilerek semantik kapsayıcılık artırılmıştır.

İkinci aşamada ise aday araçlar, cross-encoder tabanlı bir yeniden sıralama (re-ranking) modeline tabi tutulmuştur. Bu model, kullanıcı sorgusu ile her bir araç açıklamasını birlikte değerlendirerek bağlamsal uyumluluk skorları üretir. Böylece yalnızca yüzeysel benzerlik değil, anlam düzeyinde eşleşme sağlanır. En yüksek skora sahip araç seçilerek LLM’e yalnızca tek bir tool sunulmakta, bu sayede yanlış araç seçimi (false-positive) riski minimize edilmektedir.

Ek olarak sistemde bir “decision layer” uygulanmıştır. Bu katman, en iyi adayın skoruna ve diğer adaylarla olan farkına (score gap) bakarak güven seviyesi düşük durumlarda hiçbir aracın seçilmemesini sağlar. Bu mekanizma sayesinde, araç gerektirmeyen genel bilgi veya sohbet tarzı sorgularda sistem doğrudan LLM cevabına yönelir ve gereksiz tool çağrıları engellenir.

Sonuç olarak geliştirilen yapı; semantic retrieval, cross-encoder reranking ve güven tabanlı karar mekanizmasını birleştirerek klasik anahtar kelime tabanlı sistemlere kıyasla daha doğru, daha bağlamsal ve hataya dayanıklı bir araç seçimi gerçekleştirmektedir.

## Öne Çıkan Kararlar

### False-Positive Azaltımı için İki Aşamalı Tool Retrieval ve Re-Ranking Mimarisi

Sadece embedding tabanlı semantik aramaya güvenmek, özellikle doğal dildeki dolaylı ifadelerde ve benzer görünen ancak farklı amaca hizmet eden araçlar arasında false-positive sonuçlara yol açabilmektedir. Bu problemi azaltmak için projede iki aşamalı bir retrieval pipeline tasarlanmıştır.

#### 🔹 Aşama 1 — High Recall (Geniş Tarama)

İlk aşamada, araçlar zenginleştirilmiş açıklamalarıyla birlikte ChromaDB’ye gömülmüş ve `paraphrase-multilingual-MiniLM-L12-v2` modeli kullanılarak sorguya en yakın aday araçlar Top-K retrieval mantığıyla getirilmiştir.

Bu aşamanın amacı:
- yüksek recall sağlamak  
- olası tüm doğru adayları kaçırmamaktır  

#### 🔹 Aşama 2 — High Precision (Re-Ranking)

İkinci aşamada ise ilk aşamadan dönen adaylar, `cross-encoder/ms-marco-MiniLM-L-6-v2` modeli ile yeniden sıralanmıştır. Cross-Encoder, kullanıcı sorgusu ile her aday aracın açıklamasını birlikte değerlendirerek bağlamsal bir uygunluk skoru üretir.

**Cross-Encoder Skorlama Formülü:**

$$
Score = CrossEncoder(Query, Document)
$$

Bu aşama sayesinde:
- yalnızca kelime benzerliği değil  
- bağlamsal anlam (intent) üzerinden karar verilir  

#### 🔹 Decision Layer (Karar Katmanı)

Re-ranking sonrasında:

- yalnızca **en yüksek skorlu araç** LLM’e sunulur  
- düşük güven skorlarında sistem **hiç araç seçmez**  
- böylece gereksiz tool çağrıları engellenir  

#### 🔹 False-Positive Azaltma Stratejileri

Bu mimaride false-positive riskini azaltmak için:

- zenginleştirilmiş tool açıklamaları (description + examples + keywords)
- negatif örnekler (negative_examples)
- cross-encoder tabanlı bağlamsal yeniden sıralama
- tek araç seçimi (top-1 selection)
- düşük güven durumunda fallback (no-tool decision)

kullanılmıştır.

#### 🔹 Sonuç

Bu yapı sayesinde sistem:

- klasik keyword tabanlı yaklaşımlara kıyasla daha doğru  
- bağlam farkındalığı yüksek  
- hataya daha dayanıklı  

bir tool selection mekanizması sunmaktadır.


### 2. Neden LangChain Kullanılmadı?
Vaka çalışmasının amacı problemi nasıl ele aldığımızı görmek olduğundan, yönlendirme (routing) ve araç seçimi işlemleri LangChain gibi framework'lerin soyutlamalarına bırakılmamıştır. Sistem; **Pydantic** (Veri doğrulama), **OpenAI Native SDK** (Fonksiyon çağırma) ve **ChromaDB** (Vektör arama) kullanılarak tamamen şeffaf ve kontrol edilebilir bir "Pipeline" olarak tasarlanmıştır.

## Kurulum ve Çalıştırma 

### 🔹 Gereksinimler

Projenin çalıştırılabilmesi için aşağıdaki ortam gereklidir:

- Python 3.10+
- pip (Python paket yöneticisi)

---

### 🔹 Bağımlılıkların kurulması

- `pip install -r requirements.txt`

### 🔹 Model Yükleme

Proje ilk çalıştırıldığında aşağıdaki modeller otomatik olarak indirilir:

- paraphrase-multilingual-MiniLM-L12-v2 → Embedding modeli (~470MB)
- cross-encoder/ms-marco-MiniLM-L-6-v2 → Re-ranking modeli (~90MB)

Bu işlem yalnızca ilk çalıştırmada gerçekleşir.

### 🔹 Proje Yapısı

Ana bileşenler:

- tool_registry.py → Araçların vektör veritabanına (ChromaDB) kaydı
- embedding_search.py → Semantic search + cross-encoder re-ranking
- base_tool.py → Tüm tool’ların türetildiği temel sınıf
- tool_schema.py → Tool metadata ve şema tanımları
- tools/ → Tüm araç implementasyonları

### 🔹Çalıştırma

Proje aşağıdaki komut ile başlatılır:

- `python -m app.main`

Başlatıldığında sistem:

- Embedding modelini yükler
- Tool’ları ChromaDB’ye gömer
- Cross-encoder modelini yükler
- Kullanıcı sorgularını işlemeye başlar
