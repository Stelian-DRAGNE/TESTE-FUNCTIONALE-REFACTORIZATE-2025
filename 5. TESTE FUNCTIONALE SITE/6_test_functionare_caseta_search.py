
"""

    6. Test funcționare caseta 'Cauta in site ...' din pagina principală - Acest test va verifica funcționalitatea casetei 'Cauta in site ...' din pagina principală a site-ului ales pentru testare.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def slow_type(element, text: str, delay: float = 0.05):
    for ch in text:
        element.send_keys(ch)
        time.sleep(delay)


if __name__ == "__main__":
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
            time.sleep(3)
            cookie_btn.click()
        except Exception:
            logging.info("ℹ️ Butonul de cookie nu a fost găsit (probabil deja acceptat).")
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

        for i in range(4):
            driver.execute_script("window.scrollBy(0,100);")
            time.sleep(1)
        time.sleep(3)

        vezi_variante = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "VEZI VARIANTE"))
        )
        time.sleep(2)
        vezi_variante.click()
        time.sleep(3)

        for i in range(5):
            driver.execute_script("window.scrollBy(0,100);")
            time.sleep(1)
        time.sleep(2)

        for i in range(4):
            driver.execute_script("window.scrollBy(0,-100);")
            time.sleep(1)
        time.sleep(2)

        logging.info("✅ Test finalizat, browserul se va închide în 3 secunde.")
        time.sleep(3)

    except Exception as e:
        logging.error(f"❌ Eroare în test: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
