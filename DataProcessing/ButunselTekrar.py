import json

files = {
    "Çizgi Roman": "CizgiRoman.json",
    "Çocuk": "Cocuk.json",
    "Kişisel Gelişim": "KisiselGelisim.json",
    "Polisiye": "Polisiye.json",
    "Tarih": "Tarih.json"
}

book_categories = {}

for category, filename in files.items():
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            books = json.load(file)
            for book in books:
                identifier = (book['kitap adı'], book['yazar'])
                if identifier not in book_categories:
                    book_categories[identifier] = set()
                book_categories[identifier].add(category)
    except json.JSONDecodeError as e:
        print(f"Hata!")

with open('butunsel_tekrarlayan_kitaplar.txt', 'w', encoding='utf-8') as file:
    for (book_name, author), categories in book_categories.items():
        if len(categories) > 1:
            categories_list = ', '.join(categories)
            file.write(f"Kitap: {book_name} | Yazar: {author} | Kategoriler: {categories_list}\n")

print("Tüm kategoriler incelendi ve birden fazla kategoride yer alan kitaplar 'butunsel_tekrarlayan_kitaplar.txt' dosyasına yazdırıldı.")
