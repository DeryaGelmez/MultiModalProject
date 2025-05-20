#JSON dosyaları üzerinde çeşitli filtreleme işlemleri ("Bulunamadı")
import json

dosya_listesi = ["CizgiRoman.json", "Cocuk.json", "KisiselGelisim.json", "Polisiye.json", "Tarih.json"]

filtre_kriterleri = [
    ("kitap adı", "Bulunamadı"),
    ("yazar", "Bulunamadı"),
    ("arka kapak", ""),
    ("arka kapak", "Bulunamadı"),
    ("kapak URL", "Bulunamadı"),
]

for dosya_adi in dosya_listesi:
    with open(dosya_adi, 'r', encoding='utf-8') as file:
        kitaplar = json.load(file) #JSON dosyasındaki verilerden liste oluşturma

    sayaclar = {f"{anahtar}: '{deger}'": 0 for anahtar, deger in filtre_kriterleri}
    silinecekler = []

    for kitap in kitaplar:
        silinecek = False
        for anahtar, deger in filtre_kriterleri:
            if kitap.get(anahtar, "").strip() == deger:
                sayaclar[f"{anahtar}: '{deger}'"] += 1
                silinecek = True
        if silinecek:
            silinecekler.append(kitap)

    print(f"\nDosya: {dosya_adi}")
    print(f"Toplam kitap sayısı: {len(kitaplar)}")
    for kriter, adet in sayaclar.items():
        print(f'- "{kriter}" kriterine uyan kitap sayısı: {adet}')
    print(f"Toplam silinecek kitap sayısı: {len(silinecekler)}")

    temizlenmis_kitaplar = [kitap for kitap in kitaplar if kitap not in silinecekler]

    yeni_dosya_adi = dosya_adi.replace(".json", "_guncel.json")

    with open(yeni_dosya_adi, 'w', encoding='utf-8') as file:
        json.dump(temizlenmis_kitaplar, file, ensure_ascii=False, indent=4)

    print(f"Temizlenmiş veri '{yeni_dosya_adi}' dosyasına kaydedildi.")
    print(f"Kalan kitap sayısı: {len(temizlenmis_kitaplar)}")
