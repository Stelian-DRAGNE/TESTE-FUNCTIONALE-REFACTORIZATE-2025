
"""

    12. Test accesare sectiunea "RETUR/GARANTIE" si completare Formular de Retur.
        Acest test va efectua accesarea si completarea formularului online cu privire la returnarea unui produs nou comandat online, produs care la primire, prezinta urme de uzura.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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
            cookie_btn.click()
        except Exception:
            logging.info("ℹ️ Cookie deja acceptat.")
        time.sleep(2)

        hover = ActionChains(driver)
        retur_menu = driver.find_element(By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > a > i")
        hover.move_to_element(retur_menu).perform()
        time.sleep(2)

        formular_retur = driver.find_element(By.CSS_SELECTOR, "#main-menu > div > ul > li:nth-child(6) > div > ul > li:nth-child(1) > a")
        hover.move_to_element(formular_retur).perform()
        time.sleep(1)
        formular_retur.click()
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        for _ in range(6):
            driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1.1)
        time.sleep(1)

        driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        slow_type(driver.find_element(By.NAME, "name"), "DRAGNE STELIAN")
        time.sleep(1)
        slow_type(driver.find_element(By.NAME, "phone"), "0729857881")
        time.sleep(1)
        slow_type(driver.find_element(By.NAME, "email"), "stelian.dragne@yahoo.com")
        time.sleep(1)
        slow_type(driver.find_element(By.NAME, "invoice"), "2025")
        time.sleep(2)

        driver.execute_script("window.scrollBy(0,200);")
        time.sleep(1)

        select_an = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[5]/div/div[1]/form/div[5]/div/select[1]"))
        )
        select_year = Select(select_an)
        select_year.select_by_visible_text("2025")
        time.sleep(1)
        select_an.click()
        time.sleep(2)

        select_luna = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[5]/div/div[1]/form/div[5]/div/select[2]"))
        )
        select_month = Select(select_luna)
        select_month.select_by_visible_text("Octombrie")
        time.sleep(1)
        select_luna.click()
        time.sleep(2)

        select_zi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[5]/div/div[1]/form/div[5]/div/select[3]"))
        )
        select_day = Select(select_zi)
        select_day.select_by_visible_text("6")
        time.sleep(1)
        select_zi.click()
        time.sleep(2)

        slow_type(driver.find_element(By.NAME, "bank_account"), "RO XX XXXX XXXX XXXX XXXX XXXX")
        time.sleep(1)

        driver.execute_script("window.scrollBy(0,150);")
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "product"), "ANVELOPA PE SARMA CONTINENTAL CROSS KING 26, NEGRU, 58-559, 26X2.3")
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "reason"), "Anvelopa prezinta urme de uzura.")
        time.sleep(1)

        driver.execute_script("window.scrollBy(0,150);")
        time.sleep(1)

        slow_type(driver.find_element(By.NAME, "message"),
            "Solicit inlocuirea produsului ANVELOPA PE SARMA CONTINENTAL CROSS KING 26, NEGRU, 58-559, 26X2.3 cu unul nou.")
        time.sleep(1)

        gdpr_checkbox = driver.find_element(By.NAME, "agreePersonalInformation")
        gdpr_checkbox.click()
        time.sleep(2)

        trimite_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sendMessage"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trimite_btn)
        time.sleep(1)

        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(1)

        ActionChains(driver).move_to_element(trimite_btn).perform()
        time.sleep(1.5)

        driver.execute_script("arguments[0].style.transform='scale(0.97)'; arguments[0].style.transition='0.2s';", trimite_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].style.transform='scale(1)';", trimite_btn)
        logging.info(" Simulare completă de apăsare pe TRIMITE CERERE (fără trimitere reală).")

        time.sleep(2)
        logging.info("✅ Test finalizat cu succes!")

    except Exception as e:
        logging.error(f"❌ Eroare în test: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
