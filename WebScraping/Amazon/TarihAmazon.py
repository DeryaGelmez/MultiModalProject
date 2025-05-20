#Amazon Tarih
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

sayfa_no=1
kitap_sayisi=1
kitap_list = []

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
# options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
    """
})

while True:
    sayfa_url = f'https://www.amazon.com.tr/s?i=stripbooks&rh=n%3A13808221031&s=popularity-rank&fs=true&page={sayfa_no}&xpid=Ye4wBHYd8nzb9&qid=1743504082&ref=sr_pg_{sayfa_no}'
    driver.get(sayfa_url)
    time.sleep(3)

    kitap_linkleri=driver.find_elements(By.CSS_SELECTOR,'div[data-cy="title-recipe"] a.a-link-normal')
    for link in kitap_linkleri:
        url=link.get_attribute('href')
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[1]) #Kitap ayrıntılarını yeni sekmede açma
        time.sleep(3)

        try:
            kitap_adi = driver.find_element(By.ID, 'productTitle').text.strip()
            print(kitap_adi)
        except:
            kitap_adi = "Bulunamadı"

        try:
            yazar = driver.find_element(By.CSS_SELECTOR, 'span.author a').text.strip()
            print(yazar)
        except:
            yazar = "Bulunamadı"

        try:
            try:
                driver.find_element(By.CSS_SELECTOR, 'span.a-expander-prompt').click()
                time.sleep(1)
            except:
                pass
            arka_kapak = driver.find_element(By.CSS_SELECTOR, 'div.a-expander-content').text.strip()
            print(arka_kapak)
        except:
            arka_kapak = "Bulunamadı"

        try:
            img_src = driver.find_element(By.CSS_SELECTOR, 'div#imgTagWrapperId img')
            img_src.click()
            time.sleep(2)
            img_src = driver.find_element(By.CSS_SELECTOR, 'img.fullscreen').get_attribute('src')
            print(img_src)
        except:
            img_src = "Bulunamadı"

        kitap = {
            'kitap adı': kitap_adi,
            'yazar': yazar,
            'arka kapak': arka_kapak,
            'kapak URL': img_src
        }

        kitap_list.append(kitap)
        print(f"{kitap_sayisi}. kitap: {kitap_adi} \n*********************************")
        kitap_sayisi+=1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'span.s-pagination-strip')
        sayfa_no += 1
    except:
        break

with open('tarih_amazon.json', 'w', encoding='utf-8') as f:
    json.dump(kitap_list, f, ensure_ascii=False, indent=4)