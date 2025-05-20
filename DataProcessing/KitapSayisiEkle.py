#Görsel kalitesine ve kategoriye uyumuna göre yapılacak manuel görsel silme işlemlerinde kolaylık sağlaması için kitapların numaralandırılması
import json
import os

file_paths = [
    "CizgiRoman.json",
    "Cocuk.json",
    "KisiselGelisim.json",
    "Polisiye.json",
    "Tarih.json"
]

updated_books = {}

for file_path in file_paths:
    category_name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r', encoding='utf-8') as file:
        books = json.load(file)

    for idx, book in enumerate(books, start=1):
        book['kitap sayısı'] = f"{idx}"

    updated_books[category_name] = books

for category, books in updated_books.items():
    output_path = f"{category}_numarali.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

print("Tüm dosyalardaki kitaplar numaralandırıldı.")
