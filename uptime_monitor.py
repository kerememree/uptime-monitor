import requests  
import sqlite3   
import time      
from datetime import datetime 


SITES_TO_MONITOR = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.midas.com.tr",  
    "https://httpstat.us/404",   
    "https://httpstat.us/500"    
]

DB_NAME = "uptime_logs.db"
CHECK_INTERVAL = 60  


def init_db():
    
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
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] Veritabanı hazır: {DB_NAME}")


def check_site(url):
    
    try:
        start_time = time.time() 
        
        
        response = requests.get(url, timeout=5)
        
        end_time = time.time() 
        duration = round(end_time - start_time, 3) 
        
        return {
            "url": url,
            "status": response.status_code,
            "time": duration,
            "error": None
        }
    except requests.exceptions.RequestException as e:
        
        return {
            "url": url,
            "status": 0, 
            "time": 0,
            "error": str(e)
        }


def save_log(data):
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO site_logs (url, status_code, response_time, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (data['url'], data['status'], data['time'], datetime.now()))
    conn.commit()
    conn.close()


def start_monitoring():
    print("--- Uptime Monitor Başlatıldı ---")
    
    
    init_db() 

    while True:
        print(f"\n--- Kontrol Zamanı: {datetime.now().strftime('%H:%M:%S')} ---")
        
        for url in SITES_TO_MONITOR:
            result = check_site(url)
            save_log(result)
            
            
            if result['status'] == 200:
                status_msg = f"BAŞARILI ({result['status']})"
            else:
                status_msg = f"HATA ({result['status']})"
            
            print(f"{status_msg} | Süre: {result['time']}s | URL: {url}")
        
        print(f"{CHECK_INTERVAL} saniye bekleniyor...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    start_monitoring()