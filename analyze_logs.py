import sqlite3
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import pandas as pd 

DB_NAME = "uptime_logs.db"


# Kodu denerken buraya kendi gerçek mail adresini ve uygulama şifreni yazmalısın.
# DİKKAT: Gmail kullanıyorsan "Uygulama Şifresi" (App Password) oluşturman şart.
SENDER_EMAIL = "*"
SENDER_PASSWORD = "*" 
RECEIVER_EMAIL = "*" 
ALERT_THRESHOLD = 5 

def get_db_connection():
    
    return sqlite3.connect(DB_NAME)

def analyze_performance():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n--- 📊 SİTE PERFORMANS RAPORU (Ortalama Yanıt Süresi) ---")
    
    query = '''
        SELECT url, AVG(response_time) as avg_time, MAX(response_time) as max_time
        FROM site_logs 
        WHERE status_code = 200 
        GROUP BY url
        ORDER BY avg_time ASC
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'URL':<30} | {'ORTALAMA (sn)':<15} | {'EN YAVAŞ (sn)':<15}")
    print("-" * 65)
    for row in results:
        url = row[0].replace("https://", "").replace("www.", "")
        avg_time = round(row[1], 4)
        max_time = round(row[2], 4)
        print(f"{url:<30} | {avg_time:<15} | {max_time:<15}")
    
    conn.close()

def analyze_errors():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n\n--- ⚠️ HATA RAPORU (Erişilemeyen Siteler) ---")
    
    query = '''
        SELECT url, status_code, COUNT(*) as error_count, MAX(timestamp) as last_seen
        FROM site_logs
        WHERE status_code != 200
        GROUP BY url, status_code
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    error_summary = [] 
    total_error_count = 0
    
    if not results:
        print("Hiçbir sitede hata bulunamadı.")
    else:
        print(f"{'URL':<30} | {'HATA KODU':<10} | {'TEKRAR':<8} | {'SON GÖRÜLME'}")
        print("-" * 75)
        for row in results:
            url = row[0].replace("https://", "")
            code = row[1]
            count = row[2]
            last_seen = row[3]
            
            print(f"{url:<30} | {code:<10} | {count:<8} | {last_seen}")
            
            
            error_summary.append(f"- {url}: Hata Kodu {code} ({count} kez)")
            total_error_count += count

    conn.close()
    return total_error_count, error_summary

def send_alert_email(error_count, error_details_list):
    
    subject = f"UYARI: {error_count} Adet Erişim Hatası Tespit Edildi."
    
    
    details_text = "\n".join(error_details_list)
    body = f"""
    Merhaba,
    
    Sistem izleme botu (Uptime Monitor) son analizde kritik seviyede hata tespit etti.
    
    TOPLAM HATA SAYISI: {error_count} (Eşik Değer: {ALERT_THRESHOLD})
    
    DETAYLAR:
    {details_text}
    
    Lütfen sunucuları veya hedef siteleri kontrol ediniz.
    
    Kerem Emre
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
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        print(f"\n[BAŞARILI] Uyarı maili gönderildi: {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"\n[HATA] Mail gönderilemedi. Hata detayı: {e}")
        

def automated_health_check():
   
    print("\n--- OTOMATİK KONTROL BAŞLIYOR ---")
    
    
    total_errors, error_details = analyze_errors()
    
    
    print(f"\n[KARAR MEKANİZMASI] Toplam Hata: {total_errors} | Eşik: {ALERT_THRESHOLD}")
    
    if total_errors >= ALERT_THRESHOLD:
        print("DURUM: Eşik aşıldı. Alarm veriliyor...")
        send_alert_email(total_errors, error_details)
    else:
        print("🟢 DURUM: Hata sayısı eşik değerin altında.")

if __name__ == "__main__":
    automated_health_check()