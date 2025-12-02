AI Powered Uptime Monitor

Bu proje, web sitelerinin sağlık durumunu izleyen, SQL veritabanında loglayan ve İstatistiksel Anomali Tespiti (Statistical Anomaly Detection) yöntemlerini kullanarak "gizli yavaşlamaları" tespit eden akıllı bir izleme sistemidir.

Geleneksel izleme araçları sadece site çöktüğünde (HTTP 500/404) haber verirken, bu AIOps aracı, site çökmese bile normalden sapan performans düşüşlerini (Latent Anomalies) algılar ve yöneticiyi uyarır.

Kullanılan Teknolojiler

Python 3: Core scripting dili.

SQLite: Log verilerinin yapısal olarak saklanması ve sorgulanması.

SMTP (Simple Mail Transfer Protocol): Otomatik alarm (alerting) sistemi.

SQL: Performans metriklerinin analizi ve raporlanması.

Requests: HTTP protokolü üzerinden veri toplama.

Pandas: Zaman serisi analizi ve istatistiksel hesaplamalar

Özellikler

1. AI Tabanlı Anomali Tespiti

Teknoloji: Python Pandas & İstatistiksel Analiz (Z-Score Mantığı).

Mantık: Sistemin geçmiş performans verilerini (Historical Data) analiz eder. Ortalama yanıt süresinden Standard Deviation (Standart Sapma) kadar sapan istekleri "Anomali" olarak işaretler.

Fayda: Kullanıcılar şikayet etmeden önce performans darboğazlarını (bottlenecks) yakalar.

2. Veri Toplama ve SQL Loglama

Hedef siteleri belirli aralıklarla pingler.

HTTP Status Code, Response Time ve Timestamp verilerini SQLite veritabanına yapısal olarak kaydeder.

3. Akıllı Alarm Sistemi (Smart Alerting)

Sadece hata durumunda değil, anomali tespit edildiğinde de devreye girer.

SMTP protokolü üzerinden detaylı bir "Olay Raporu" (Incident Report) gönderir.