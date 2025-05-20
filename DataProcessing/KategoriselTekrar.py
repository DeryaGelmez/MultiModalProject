#Dosyaların herbirinde tekrar eden kitapların birbirinden bağımsız olarak tespit edilmesi
import json

dosya_listesi = ["CizgiRoman.json", "Cocuk.json", "KisiselGelisim.json", "Polisiye.json", "Tarih.json"]
tekrar_edenler_dosya = "tekrarlayan_kitaplar.txt"

with open(tekrar_edenler_dosya, 'w', encoding='utf-8') as file:
    file.write("Tekrarlayan Kitaplar Raporu\n\n")

for dosya_adi in dosya_listesi:

    with open(dosya_adi, 'r', encoding='utf-8') as file:
        kitaplar = json.load(file)

    gorulen_kitaplar = set()
    tekrar_eden_kitaplar = set()
    benzersiz_kitaplar = []

    for kitap in kitaplar:
        kitap_adi = kitap.get("kitap adı", "").strip()
        yazar = kitap.get("yazar", "").strip()
        kitap_kimligi = f"{kitap_adi} - {yazar}"
        if kitap_kimligi in gorulen_kitaplar:
            tekrar_eden_kitaplar.add(kitap_kimligi)
        else:
            gorulen_kitaplar.add(kitap_kimligi)
            benzersiz_kitaplar.append(kitap)
    yeni_dosya_adi = dosya_adi.replace(".json", "_guncel.json")

    with open(yeni_dosya_adi, 'w', encoding='utf-8') as file:
        json.dump(benzersiz_kitaplar, file, ensure_ascii=False, indent=4)

    with open(tekrar_edenler_dosya, 'a', encoding='utf-8') as file:
        file.write(f"Kategori: {dosya_adi}\n")
        file.write(f"Toplam kitap sayısı: {len(kitaplar)}\n")
        file.write(f"Tekrar eden kitap sayısı: {len(tekrar_eden_kitaplar)}\n")
        file.write(f"Kalan benzersiz kitap sayısı: {len(benzersiz_kitaplar)}\n")

        if tekrar_eden_kitaplar:
            file.write("\nTekrar eden kitaplar (Kitap Adı - Yazar):\n")
            for kitap_kimligi in tekrar_eden_kitaplar:
                file.write(f"- {kitap_kimligi}\n")
        else:
            file.write("Tekrar eden kitap bulunamadı.\n")
        file.write("\n" + "-" * 50 + "\n\n")
    print(f"'{dosya_adi}' dosyası kontrol edildi. Temiz dosya: '{yeni_dosya_adi}'")
print(f"\nTüm tekrarlayan kitaplar '{tekrar_edenler_dosya}' dosyasına kaydedildi.")
