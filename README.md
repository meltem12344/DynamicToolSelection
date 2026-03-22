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

### 1. False-Positive Azaltımı için İki Aşamalı Tool Retrieval ve Re-Ranking Mimarisi

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


## 📊 Örnek Sistem Çıktıları (Console Log)




## ⚙️ Kurulum ve Çalıştırma 

### 1. Gereksinimler

Projeyi çalıştırmadan önce aşağıdakilerin kurulu olması gerekir:

- Python 3.10 veya üzeri
- Git
- OpenAI API anahtarı (eğer proje içinde OpenAI istemcisi kullanılıyorsa)

Kontrol etmek için:

- `python --version`
- `git --version`

### 2. Projeyi GitHub’dan İndirme

Terminal açılır ve proje klonlanır:

- `git clone https://github.com/meltem12344/DynamicToolSelection`

Klasöre girilir:

- `cd DynamicToolSelection`
  
### 3. Sanal Ortam Oluşturma

Windows

- `python -m venv venv`
- `venv\Scripts\activate`

Mac / Linux

- `python3 -m venv venv`
- `source venv/bin/activate`

Aktifleştirme sonrası terminal başında genelde (venv) görünür.

### 4. Bağımlılıkların Kurulumu

- `pip install -r requirements.txt`

### 5. API Key Ayarı

Bu projede gerçek API anahtarları güvenlik nedeniyle GitHub’a yüklenmez.
Bu yüzden kullanıcı kendi .env dosyasını oluşturmalıdır.

Proje kök dizininde .env dosyası oluştur:

Windows

- `notepad .env`

Mac / Linux

- `touch .env`
- `nano .env`

İçine şunu yaz:

OPENAI_API_KEY=your_api_key_here


### 7. İlk Çalıştırmada Model İndirmeleri

Proje ilk kez çalıştırıldığında aşağıdaki modeller otomatik olarak indirilebilir:

- `paraphrase-multilingual-MiniLM-L12-v2` → embedding modeli
- `cross-encoder/ms-marco-MiniLM-L-6-v2` → re-ranking modeli

Bu indirme işlemi ilk çalıştırmada normalden daha uzun sürebilir.
Sonraki çalıştırmalarda daha hızlı açılır.

### 8. Proje Yapısı

Önemli dosyalar:

- `app/main.py` → ana giriş noktası
- `app/tools/tool_registry.py` → tool’ların ChromaDB’ye kaydı
- `app/tools/base_tool.py` → tüm tool’ların temel sınıfı
- `app/schemas/tool_schema.py` → tool schema ve metadata tanımları
- `app/search/embedding_search.py` veya benzeri → semantic search + re-ranking mantığı
- `app/tools/` → tüm tool implementasyonları

### 9. Projeyi Çalıştırma

Ana dizinde şu komut çalıştırılır:

- `python -m app.main`

Başlatıldığında sistem tipik olarak şu adımları yapar:

1. Embedding modelini yükler
2. Tool’ları ChromaDB’ye gömer
3. Cross-encoder modelini yükler
4. Kullanıcı sorgularını işlemeye başlar

### 10. Örnek Test Sorguları

Kurulum sonrası aşağıdaki sorgularla sistem test edilebilir:

      Bugün Ankara'da hava kaç derece?
      256 ile 48'i çarpar mısın?
      "Bugün hava çok güzel" cümlesini İngilizceye çevir.
      150 doları Türk Lirasına çevir.
      Yarın saat 14:00 için toplantı ekle.
      20 dakikalık bir zamanlayıcı başlat.
      Ahmet'e "Toplantı yarın" konulu bir e-posta gönder.
      X kullanıcısının toplam kaç sipariş verdiğini öğrenmek istiyorum.
      https://example.com adresindeki belgeyi okuyup özetle.
      Yapay zeka hakkında güncel haberleri internette ara.

### 11. Notlar

Bu proje:

- modüler tool mimarisi kullanır
- semantic search tabanlı tool routing yapar
- cross-encoder ile re-ranking uygular
- açıklama, örnek ve metadata tabanlı tool temsilinden yararlanır

Yeni bir tool eklemek için genel akış:

1. `BaseTool` sınıfından türeyen yeni bir tool oluştur
2. `schema` alanını doldur
3. `execute()` metodunu yaz
4. Tool’u `ToolRegistry` içine register et

### 🔹 Kısa Kurulum Özeti

Hızlı kurulum için:

```bash
git clone https://github.com/KULLANICI_ADIN/REPO_ADIN.git
cd REPO_ADIN
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

.env dosyası oluştur:

OPENAI_API_KEY=your_api_key_here

Projeyi çalıştır:

python -m app.main
