#DR Tüm Kategoriler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

categories = [
{"name": "kisiselgelisim",
     "url": "https://www.dr.com.tr/kategori/Kitap/Egitim-Basvuru/Kisisel-Gelisim/grupno=00179?Page={sayfa_no}&ShowNotForSale=false"},
    {"name": "cocuk",
     "url": "https://www.dr.com.tr/kategori/Kitap/Cocuk-ve-Genclik/Okul-Cagi-6-10-Yas/grupno=00886?Page={sayfa_no}&ShowNotForSale=false"},
    {"name": "tarih",
     "url": "https://www.dr.com.tr/kategori/Kitap/Arastirma-Tarih/Tarih/grupno=00226?Page={sayfa_no}&ShowNotForSale=false"},
    {"name": "cizgiroman",
     "url": "https://www.dr.com.tr/kategori/Kitap/Cizgi-Roman/grupno=00053?Page={sayfa_no}&ShowNotForSale=false"},
    {"name": "polisiye",
     "url": "https://www.dr.com.tr/kategori/Kitap/Edebiyat/Roman/Polisiye/grupno=00497?Page={sayfa_no}&ShowNotForSale=false"}
]

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

for category in categories:
    sayfa_no=1
    kitap_sayisi=1
    kitap_list = []
    part = 1  #Her 500 kitapta bir JSON dosyası oluşturmak için

    while kitap_sayisi<=6000:
        sayfa_url = category["url"].format(sayfa_no=sayfa_no)
        driver.get(sayfa_url)
        time.sleep(3)
        kitap_linkleri=driver.find_elements(By.CSS_SELECTOR,'div.prd-infos')
        if not kitap_linkleri:
            break
        for link in kitap_linkleri:
            if kitap_sayisi > 6000:
                break
            try:
                kitap_link=link.find_element(By.CSS_SELECTOR,'a')
                url=kitap_link.get_attribute('href')
                driver.execute_script("window.open(arguments[0]);", url)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)

                try:
                    kitap_adi = driver.find_element(By.CSS_SELECTOR, 'div.prd-name').text.strip()
                    print(f"Kitap Adı: {kitap_adi}")
                except:
                    kitap_adi = "Bulunamadı"

                try:
                    yazar = driver.find_element(By.CSS_SELECTOR, 'h2.author a').text.strip()
                    print(f"Yazar: {yazar}")
                except:
                    yazar = "Bulunamadı"

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.js-detail-product'))
                    )
                    arka_kapak = driver.execute_script(
                        "return document.querySelector('div.js-detail-product').innerText;"
                    ).strip()
                    print(f"Arka kapak yazısı: {arka_kapak}")
                except Exception as e:
                    print("Hata oluştu:", e)
                    arka_kapak = "Bulunamadı"

                try:
                    img_url = driver.find_element(By.CSS_SELECTOR, 'div.swiper-slide-active img').get_attribute('src')
                    print(f"Görsel URL: {img_url}")
                except:
                    img_url = "Bulunamadı"

                kitap = {
                    'kitap adı': kitap_adi,
                    'yazar': yazar,
                    'arka kapak': arka_kapak,
                    'kapak URL': img_url
                }

                kitap_list.append(kitap)
                print(f"({sayfa_no}. sayfa {kitap_sayisi}. kitap)\n********************************** ")
                kitap_sayisi+=1

                if kitap_sayisi % 500 == 0:
                    filename = f"{category['name']}_part{part}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(kitap_list, f, ensure_ascii=False, indent=4)
                    print(f"\n✔ {filename} dosyasına {len(kitap_list)} kitap kaydedildi.\n")
                    kitap_list = []
                    part += 1

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Hata oluştu: {e}")
                driver.switch_to.window(driver.window_handles[0])
                continue

        if kitap_sayisi > 6000:
            break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next a')
            sayfa_no += 1
        except:
            break

    if kitap_list:
        filename = f"{category['name']}_part{part}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(kitap_list, f, ensure_ascii=False, indent=4)
        print(f"\n→ {filename} dosyasına kalan {len(kitap_list)} kitap kaydedildi.\n")

driver.quit()