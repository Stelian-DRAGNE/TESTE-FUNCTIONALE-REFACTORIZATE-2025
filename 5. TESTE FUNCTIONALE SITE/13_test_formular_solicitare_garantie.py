
"""

    13. Test accesare sectiunea "RETUR/GARANTIE" si completare Formular de Garantie.
        Acest test va efectua accesarea si completarea formularului online cu privire la aplicarea conditiilor de garantie comerciala asupra unui produs nou, putin utilizat, care prezinta diverse neconcordante functionale si de forma.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
            logging.info("ℹ️ Cookie deja acceptat sau deja acceptat anterior.")
        time.sleep(2)

        actions = ActionChains(driver)

        menu_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > a > i"))
        )
        actions.move_to_element(menu_icon).pause(1).perform()
        time.sleep(1.5)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > div > ul"))
        )
        time.sleep(1)

        formular_garantie = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > div > ul > li:nth-child(2) > a"))
        )
        actions.move_to_element(formular_garantie).pause(1.5).perform()
        time.sleep(1.5)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > div > ul > li:nth-child(2) > a")))
        formular_garantie.click()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)

        for i in range(5):
            driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1)
        time.sleep(2)

        slow_type(driver.find_element(By.NAME, "name"), "DRAGNE STELIAN", delay=0.05)
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "phone"), "0729857881", delay=0.05)
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "email"), "stelian.dragne@yahoo.com", delay=0.05)
        time.sleep(1)

        driver.execute_script("window.scrollBy(0,175)")
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "invoice"), "2025", delay=0.05)
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "invoice_date"), "06.10.2025", delay=0.05)
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "product"), "BICICLETA ROCK MACHINE CROSSRIDE 100 29'' NEGRU/ROSU M-18''", delay=0.05)
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "message"), "Cadrul bicicletei este strâmb, roata spate este ovala și ghidonul se mișcă greu stânga-dreapta.", delay=0.05)
        time.sleep(2)

        driver.execute_script("window.scrollBy(0,175)")
        time.sleep(1)

        gdpr = driver.find_element(By.NAME, "agreePersonalInformation")
        gdpr.click()
        time.sleep(1)

        trimite_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sendMessage"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trimite_btn)
        time.sleep(1)
        actions.move_to_element(trimite_btn).perform()

        driver.execute_script("""
            arguments[0].style.transition='0.3s';
            arguments[0].style.transform='scale(0.95)';
            arguments[0].style.backgroundColor='rgba(255,0,0,0.3)';
        """, trimite_btn)
        time.sleep(0.5)
        driver.execute_script("""
            arguments[0].style.transform='scale(1)';
            arguments[0].style.backgroundColor='';
        """, trimite_btn)

        time.sleep(3)
        logging.info("✅ Test finalizat cu succes!")

    except Exception as e:
        logging.error(f"❌ Eroare în execuție: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
