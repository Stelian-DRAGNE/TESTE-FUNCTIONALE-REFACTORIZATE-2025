
"""

    8.  Test cautare produs 2 in caseta 'Cauta in site ...' și test adaugare produs 2 in cos, urmate de simulare finalizare comandă - Acest test va efectua cautarea unui produs în cadrul site-ului ales pentru testare, se va accesa produsul respectiv, se adaugă în coș. În continuare se va efectua cautarea unui alt produs în cadrul site-ului ales pentru testare, se va accesa produsul respectiv, se adaugă în coș și se simuleaza finalizarea comenzii pentru cele doua produse alese.

"""



import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def slow_type(element, text: str, delay: float = 0.05):
    if not text: 
        return
    for ch in str(text):
        element.send_keys(ch)
        time.sleep(delay)


if __name__ == "__main__":
    load_dotenv("8.comanda_2.env")
    EMAIL = str(os.getenv("EMAIL", ""))
    FIRST_NAME = str(os.getenv("FIRST_NAME", ""))
    LAST_NAME = str(os.getenv("LAST_NAME", ""))
    PHONE = str(os.getenv("PHONE", ""))
    ADRESS = str(os.getenv("ADRESS", ""))
    PC = str(os.getenv("P.C.", ""))

    if not all([EMAIL, FIRST_NAME, LAST_NAME, PHONE, ADRESS, PC]):
        raise ValueError("❌ Lipsesc variabile în 8.comanda_2.env (EMAIL, FIRST_NAME, LAST_NAME, PHONE, ADRESS, P.C.)!")

    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get("https://www.mosionroata.ro/")
        time.sleep(2)

        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy"))
            )
            time.sleep(2)
            cookie_btn.click()
        except Exception:
            logging.info("ℹ️ Cookie nu a fost găsit (probabil deja acceptat).")
        time.sleep(2)

        search_produs = "Bicicleta MTB Rock Machine Whizz FS III 90 AXS 27.5, sulfur yellow, cadru 41cm"
        caseta_cautare = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "c"))
        )
        slow_type(caseta_cautare, search_produs, delay=0.05)

        lupa_icon = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.search-button"))
        )
        ActionChains(driver).move_to_element(lupa_icon).perform()
        time.sleep(5)

        caseta_cautare.send_keys(Keys.RETURN)
        time.sleep(3)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)
        vezi_variante = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "VEZI VARIANTE"))
        )
        time.sleep(3)
        vezi_variante.click()
        time.sleep(3)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)

        adauga_in_cos = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#product-page > div.container-h.product-top.-g-product-60361 > "
                "div.row.-g-product-row-box > div.col-sm-6.detail-prod-attr.pull-right.-g-product-details > "
                "div.add-section.clearfix.-g-product-add-section-60361 > a"
            ))
        )
        adauga_in_cos.click()
        time.sleep(6)

        try:
            close_popup = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                    "#fancybox-container-1 > div.fancybox-inner > div.fancybox-stage > "
                    "div > div > button > svg > path"
                ))
            )
            close_popup.click()
        except Exception:
            logging.warning("⚠️ Nu s-a găsit popup-ul pentru închidere (poate s-a închis automat).")
        time.sleep(2)

        search_produs_2 = "Anvelopa pliabila Continental Cross King ShieldWall 55-584"
        caseta_cautare = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "c"))
        )
        caseta_cautare.clear()
        time.sleep(1)

        slow_type(caseta_cautare, search_produs_2, delay=0.05)
        lupa_icon = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.search-button"))
        )
        ActionChains(driver).move_to_element(lupa_icon).perform()
        time.sleep(5)

        caseta_cautare.send_keys(Keys.RETURN)
        time.sleep(3)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)

        vezi_variante_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "VEZI VARIANTE"))
        )
        time.sleep(3)
        vezi_variante_2.click()
        time.sleep(3)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)

        dimensiune_anvelopa = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#product-page > div.container-h.product-top.-g-product-10505 > div.row.-g-product-row-box > div.col-sm-6.detail-prod-attr.pull-right.-g-product-details > div:nth-child(7) > div > div.attribute-dimensiune_anvelopa > div:nth-child(4) > a"
            ))
        )
        time.sleep(2)
        dimensiune_anvelopa.click()
        time.sleep(2)

        qty_plus = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qtyplus > i"))
        )
        time.sleep(2)
        qty_plus.click()
        time.sleep(2)

        adauga_in_cos_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#product-page > div.container-h.product-top.-g-product-13873 > div.row.-g-product-row-box > div.col-sm-6.detail-prod-attr.pull-right.-g-product-details > div.add-section.clearfix.-g-product-add-section-13873 > a"
            ))
        )
        adauga_in_cos_2.click()
        time.sleep(5)

        finalizeaza_comanda_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#fancybox-container-1 > div.fancybox-inner > div.fancybox-stage > "
                "div > div > div > div.widget-custom-button-holder > a.btn.btn-cmd"
            ))
        )
        finalizeaza_comanda_2.click()
        time.sleep(3)

        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#checkoutform > div:nth-child(2) > div.col-xs-8 > label > div > input"
            ))
        )
        checkbox.click()
        time.sleep(1)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#checkoutform > div:nth-child(4) > input"))
        )
        slow_type(email_input, EMAIL, delay=0.05)
        time.sleep(2)

        nume_input = driver.find_element(By.CSS_SELECTOR, "#checkoutform > div:nth-child(5) > input")
        slow_type(nume_input, LAST_NAME, delay=0.05)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,150);")
        time.sleep(1)

        prenume_input = driver.find_element(By.CSS_SELECTOR, "#checkoutform > div:nth-child(6) > input")
        slow_type(prenume_input, FIRST_NAME, delay=0.05)
        time.sleep(2)

        phone_input = driver.find_element(By.CSS_SELECTOR, "#__orderCkeckoutPhoneNumber")
        slow_type(phone_input, PHONE, delay=0.05)
        time.sleep(2)

        for i in range(2):
            driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1)

        judet_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#_shippingRegion"))
        )
        judet_select.click()
        time.sleep(2)

        localitate_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#_shippingCity"))
        )
        select_loc = Select(localitate_select)
        select_loc.select_by_index(2)  
        time.sleep(1)
        localitate_select.click()
        time.sleep(2)

        adresa_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "#_shippingAddressHolder > input.input-s.col-sm-5.col-xs-8.-g-storage"
            ))
        )
        slow_type(adresa_input, ADRESS, delay=0.05)
        time.sleep(1)

        cod_postal_input = driver.find_element(By.CSS_SELECTOR, "#_shippingZipcode")
        slow_type(cod_postal_input, PC, delay=0.05)
        time.sleep(1)

        livrare_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#checkoutform > div.form-h.-g-checkout-delivery-method-section > div > label:nth-child(1) > input"
            ))
        )
        livrare_radio.click()
        time.sleep(2)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)

        plata_card = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#_paymentOptions > span.-g-payment-method.-g-payment-method-8 > label > input"
            ))
        )
        plata_card.click()
        time.sleep(1)

        mesajul_tau = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "#checkoutform > div:nth-child(29) > textarea"
            ))
        )
        slow_type(mesajul_tau, "Va multumesc pentru operativitate si seriozitate.", delay=0.05)
        time.sleep(1)

        for i in range(3):
            driver.execute_script("window.scrollBy(0,150);")
            time.sleep(1)

        checkbox1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#checkoutform > div:nth-child(32) > label > div > input"
            ))
        )
        checkbox1.click()
        time.sleep(1)

        checkbox2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#checkoutform > div:nth-child(33) > label > div > input"
            ))
        )
        checkbox2.click()
        time.sleep(1)

        driver.execute_script("window.scrollBy(0,150);")
        time.sleep(1)

        trimite_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#doCheckout"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trimite_btn)
        time.sleep(1)

        driver.execute_script("window.scrollBy(0, -50);")
        time.sleep(1)

        ActionChains(driver).move_to_element(trimite_btn).perform()
        time.sleep(2)

        logging.info("🎉 Test finalizat cu succes!")

    except Exception as e:
        logging.error(f"❌ Eroare în test: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
