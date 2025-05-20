#Görsel hash değerlerinin hesaplanmasıyla tekrar eden kitapların tespiti
import os
from PIL import Image
import imagehash

base_dir = r"/Datas"
folders = ["Çizgi Roman", "Çocuk", "Kişisel Gelişim", "Polisiye", "Tarih"]

hash_dict = {}
duplicates = {}

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    for file in os.listdir(folder_path):
        if file.lower().endswith(".jpg"):
            file_path = os.path.join(folder_path, file)
            try:
                img = Image.open(file_path)
                img_hash = str(imagehash.dhash(img))

                if img_hash in hash_dict:
                    if img_hash not in duplicates:
                        duplicates[img_hash] = [hash_dict[img_hash]]
                    duplicates[img_hash].append(file_path)
                else:
                    hash_dict[img_hash] = file_path
            except Exception as e:
                print(f"Hata: {file_path} - {e}")

output_path = os.path.join(base_dir, "tekrar_gorseller.txt")
with open(output_path, "w", encoding="utf-8") as f:
    if not duplicates:
        f.write("Hiçbir tekrar görsel bulunamadı.\n")
    else:
        for i, (h, paths) in enumerate(duplicates.items(), 1):
            f.write(f"[{i}] Tekrar Görsel Hash: {h}\n")
            for p in paths:
                f.write(f"    - {p}\n")
            f.write("\n")

print(f"\nİşlem tamamlandı. Tekrar görseller 'tekrar_gorseller.txt' dosyasına kaydedildi.")
