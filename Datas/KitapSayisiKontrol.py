import json

with open("Tarih.json", "r", encoding="utf-8") as file:
    kitaplar = json.load(file)

print(f"Toplam kitap sayısı: {len(kitaplar)}")
