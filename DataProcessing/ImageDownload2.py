#Kitapların numaralandırılarak indirilmesi
import os
import json
import requests

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
    log_file.write("İndirilemeyen Kitap Kapakları:\n\n")

for folder in files.values():
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

for json_file, folder in files.items():
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for kitap in data:
            url = kitap.get("kapak URL")
            kitap_sayisi = kitap.get("kitap sayısı")
            if url and kitap_sayisi:
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        image_path = os.path.join(base_dir, folder, f"{kitap_sayisi}.jpg")
                        with open(image_path, "wb") as img_file:
                            img_file.write(response.content)
                        print(f"İndirildi: {image_path}")
                    else:
                        raise Exception(f"HTTP {response.status_code}")
                except Exception as e:
                    with open(log_file_path, "a", encoding="utf-8") as log_file:
                        log_file.write(f"{kitap.get('kitap adı')} ({folder}) → {url} | Hata: {e}\n")
            else:
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(f"{kitap.get('kitap adı')} ({folder}) → Geçersiz veri\n")

    except Exception as e:
        print(f"HATA: {json_file} okunamadı → {e}")
