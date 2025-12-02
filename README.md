Website Uptime & Performance Monitor

Bu proje, belirlenen web sitelerinin erişilebilirliğini (uptime) ve yanıt sürelerini (response time) 7/24 izleyen, verileri SQL veritabanında saklayan ve kritik durumlarda otomatik e-posta bildirimi gönderen bir Python otomasyon aracıdır.

Projenin Amacı

Test Mühendisliği ve SRE (Site Reliability Engineering) pratiklerini uygulamak amacıyla geliştirilmiştir. Manuel kontroller yerine, sistemin sağlık durumunu otomatize edilmiş scriptlerle izlemeyi hedefler.

Kullanılan Teknolojiler

Python 3: Core scripting dili.

SQLite: Log verilerinin yapısal olarak saklanması ve sorgulanması.

SMTP (Simple Mail Transfer Protocol): Otomatik alarm (alerting) sistemi.

SQL: Performans metriklerinin analizi ve raporlanması.

Requests: HTTP protokolü üzerinden veri toplama.

Özellikler

1. Veri Toplama (Monitoring)

Hedef sitelere HTTP GET istekleri atar.

Yanıt sürelerini (latency) milisaniye cinsinden ölçer.

HTTP Durum Kodlarını (200, 404, 500 vb.) analiz eder.

Bağlantı hatalarını (Connection Error) yakalar ve loglar.

2. Veri Analizi ve Raporlama

Toplanan verileri SQLite veritabanına yazar.

SQL sorguları ile sitelerin ortalama açılma hızlarını hesaplar.

Hata oranlarını analiz eder.

3. Otomatik Alarm Sistemi (Alerting)

Sistemdeki hata sayısı belirlenen eşik değeri (Threshold) geçerse devreye girer.

Yöneticiye, hata detaylarını içeren bir e-posta gönderir.