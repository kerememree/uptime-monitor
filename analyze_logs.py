
import sys
import subprocess
import pandas as pd
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
from datetime import datetime, timedelta


DB_NAME = "uptime_logs.db"


SENDER_EMAIL = "***"
SENDER_PASSWORD = "***"
RECEIVER_EMAIL = "***"


ANOMALY_STD_DEV_FACTOR = 2.0  
MIN_DATA_POINTS = 5           


def create_dummy_data_if_not_exists():

    if os.path.exists(DB_NAME):
        return

    print(" Veritabanı bulunamadı. Test için SAHTE VERİ oluşturuluyor...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    print(" Midas sitesi için normal veriler ekleniyor (0.2s - 0.5s arası)...")
    for _ in range(20):
        t = random.uniform(0.2, 0.5)
        cursor.execute("INSERT INTO site_logs (url, status_code, response_time) VALUES (?, ?, ?)", 
                       ("midas.com.tr", 200, t))
    
    
    print(" Midas sitesi için ANOMALİ verisi ekleniyor (2.5s!)...")
    cursor.execute("INSERT INTO site_logs (url, status_code, response_time) VALUES (?, ?, ?)", 
                   ("midas.com.tr", 200, 2.5))

    
    for _ in range(10):
        t = random.uniform(0.1, 0.3)
        cursor.execute("INSERT INTO site_logs (url, status_code, response_time) VALUES (?, ?, ?)", 
                       ("google.com", 200, t))

    conn.commit()
    conn.close()
    print(" Test veritabanı hazır!\n")


def get_db_connection():
    return sqlite3.connect(DB_NAME)


def detect_anomalies():
    conn = get_db_connection()
    
    
    query = "SELECT url, response_time FROM site_logs WHERE status_code = 200"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return []

    anomalies = []
    
    print(f"\n ---  PERFORMANS ANALİZİ ---")
    print(f"{'URL':<20} | {'ORTALAMA':<10} | {'ŞU AN':<10} | {'DURUM'}")
    print("-" * 60)

    for url in df['url'].unique():
        site_data = df[df['url'] == url]
        
        if len(site_data) < MIN_DATA_POINTS:
            continue
            
        
        mean_time = site_data['response_time'].mean()
        std_dev = site_data['response_time'].std()
        
        
        last_entry_time = site_data.iloc[-1]['response_time']
        
        
        limit = mean_time + (ANOMALY_STD_DEV_FACTOR * std_dev)
        
        is_anomaly = last_entry_time > limit
        status = " ANOMALİ" if is_anomaly else " NORMAL"
        
        print(f"{url:<20} | {mean_time:.3f}s     | {last_entry_time:.3f}s     | {status}")
        
        if is_anomaly:
            msg = f"- {url}: Yanıt süresi {last_entry_time:.2f}s (Normali: {mean_time:.2f}s). Beklenmedik yavaşlama!"
            anomalies.append(msg)
            
    return anomalies


def analyze_errors():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    cursor.execute('''
        SELECT url, status_code, COUNT(*) 
        FROM site_logs 
        WHERE status_code != 200 
        GROUP BY url, status_code
    ''')
    results = cursor.fetchall()
    conn.close()
    
    error_summary = []
    total_count = 0
    for row in results:
        error_summary.append(f"- {row[0]}: Hata Kodu {row[1]} ({row[2]} kez)")
        total_count += row[2]
        
    return total_count, error_summary


def send_smart_alert(error_count, error_details, anomaly_details):
    print("\n  Rapor oluşturuluyor...")
    
    # E-mail ayarları boşsa sadece ekrana yazıp çıkalım
    if "gmail.com" not in SENDER_EMAIL or "sifre" in SENDER_PASSWORD:
        print(" E-mail ayarları yapılmadığı için mail gönderilemedi (Console Log Sadece).")
        print(" DETAYLAR:")
        if error_details: print("Hatalar:\n" + "\n".join(error_details))
        if anomaly_details: print("Anomaliler:\n" + "\n".join(anomaly_details))
        return

    subject = " Uyarı: Sistemde Düzensizlik Tespit Edildi"
    body = f"""
    Sistem İzleme Raporu
    --------------------
    
    1. ERİŞİM HATALARI:
    Toplam: {error_count}
    {chr(10).join(error_details) if error_details else "Yok."}
    
    2. PERFORMANS ANOMALİLERİ (AI Tespiti):
    {chr(10).join(anomaly_details) if anomaly_details else "Yok."}
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f" Mail başarıyla gönderildi: {RECEIVER_EMAIL}")
    except Exception as e:
        print(f" Mail gönderme hatası: {e}")


if __name__ == "__main__":
    # 1. Test verisi oluştur (Sadece veritabanı yoksa çalışır)
    create_dummy_data_if_not_exists()
    
    print("\n---  KONTROL BAŞLIYOR ---")
    
    # 2. Hataları Analiz Et
    err_count, err_details = analyze_errors()
    
    # 3. Anomalileri Tespit Et
    anomalies = detect_anomalies()
    
    # 4. Sonuç
    if err_count > 0 or anomalies:
        send_smart_alert(err_count, err_details, anomalies)
    else:
        print("\n SİSTEM STABİL: Herhangi bir sorun tespit edilmedi.")