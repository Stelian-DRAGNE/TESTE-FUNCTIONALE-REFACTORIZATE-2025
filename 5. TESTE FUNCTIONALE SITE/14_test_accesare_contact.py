
"""

    14. Test accesare sectiunea "CONTACT".
        Acest test va efectua accesarea sectiunii "CONTACT", sectiune prezenta in cadrul site-ului ales pentru testare si completarea formuralui on-line disponibil.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def slow_type(element, text, delay=0.05):
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
            cookie_btn.click()
        except:
            logging.info("ℹ️ Cookie deja acceptat sau absent.")
        time.sleep(2)

        contact_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(7) > a"))
        )
        contact_link.click()
        time.sleep(2)

        for i in range(4):
            driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1.1)
        time.sleep(2)

        driver.execute_script("window.scrollTo(0,450);")
        time.sleep(2)

        email = "stelian.dragne@yahoo.com"
        email_field = driver.find_element(By.ID, "email")
        slow_type(email_field, email, delay=0.05)
        time.sleep(1)

        nume = "STELIAN DRAGNE"
        nume_field = driver.find_element(By.NAME, "lastname")
        slow_type(nume_field, nume, delay=0.05)
        time.sleep(1)

        telefon = "0729857881"
        telefon_field = driver.find_element(By.NAME, "phone")
        slow_type(telefon_field, telefon, delay=0.05)
        time.sleep(1)

        driver.execute_script("window.scrollBy(0,125);")
        time.sleep(1)

        mesaj = "Va rog sa ma contactati cat mai repede posibil. Comanda mea inca nu a fost livrata."
        mesaj_field = driver.find_element(By.NAME, "message")
        slow_type(mesaj_field, mesaj, delay=0.05)
        time.sleep(1)

        gdpr_checkbox = driver.find_element(By.NAME, "agreePersonalInformation")
        gdpr_checkbox.click()
        time.sleep(1)

        trimite_btn = driver.find_element(By.ID, "sendMessage")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trimite_btn)
        time.sleep(1)

        ActionChains(driver).move_to_element(trimite_btn).perform()

        driver.execute_script("""
            arguments[0].style.transition='0.3s';
            arguments[0].style.transform='scale(0.95)';
            arguments[0].style.backgroundColor='rgba(0,128,0,0.3)';
        """, trimite_btn)
        time.sleep(0.5)
        driver.execute_script("""
            arguments[0].style.transform='scale(1)';
            arguments[0].style.backgroundColor='';
        """, trimite_btn)

        logging.info("✅ Test finalizat cu succes !")

        time.sleep(3)

    except Exception as e:
        logging.error(f"❌ Eroare în execuție: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
