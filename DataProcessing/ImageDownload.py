#Tekrarlayan kitapların tespiti için kitap adıyla indirme
import os
import json
import requests
import re

files = {
    "CizgiRoman.json": "Çizgi Roman",
    "Cocuk.json": "Çocuk",
    "KisiselGelisim.json": "Kişisel Gelişim",
    "Polisiye.json": "Polisiye",
    "Tarih.json": "Tarih"
}

base_dir = os.getcwd()

log_file_path = os.path.join(base_dir, "indirilemeyenler.txt")

with open(log_file_path, "w", encoding="utf-8") as log_file:
    log_file.write("İndirilemeyen Kitaplar Raporu\n\n")

for folder in files.values():
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

def temiz_dosya_adi(ad):
    return re.sub(r'[<>:"/\\|?*]', '', ad).strip()

def download_image(image_url, save_path, kitap_adi, kategori):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"İndirildi: {save_path}")
            return True
        else:
            raise Exception()
    except:
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{kategori}] {kitap_adi}\nURL: {image_url}\n\n")
        print(f"İndirilemedi: {kitap_adi} ({kategori})")
        return False

for file_name, folder_name in files.items():
    file_path = os.path.join(base_dir, file_name)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            books = json.load(f)
    except Exception as e:
        print(f"Dosya okunamadı: {file_name} → {e}")
        continue

    for book in books:
        kitap_adi = book.get("kitap adı", "").strip()
        yazar = book.get("yazar", "").strip()
        image_url = book.get("kapak URL", "").strip()

        if not kitap_adi or not image_url:
            print(f"Eksik bilgi: {kitap_adi or 'Bilinmeyen'}")
            continue

        # Benzersiz dosya adı: kitap adı - yazar
        dosya_ad_metni = f"{kitap_adi} - {yazar}" if yazar else kitap_adi
        dosya_adi = temiz_dosya_adi(dosya_ad_metni) + ".jpg"
        save_path = os.path.join(base_dir, folder_name, dosya_adi)

        download_image(image_url, save_path, kitap_adi, folder_name)

print("\n✅ Tüm görseller işlendi. İndirilemeyenler 'indirilemeyenler.txt' dosyasına kaydedildi.")
