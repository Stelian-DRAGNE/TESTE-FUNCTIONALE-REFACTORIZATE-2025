
"""

    15. Test abonare la 'Newsletter'.
        Acest test va efectua abonarea la 'Newsletter', sectiune prezenta in cadrul site-ului ales pentru testare.

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

        for i in range(30):
            driver.execute_script("window.scrollBy(0,200);")
            time.sleep(1.1)
        driver.execute_script("window.scrollTo(5250,5250);")
        time.sleep(3)

        email = "stelian.dragne@yahoo.com"
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "_emailAddress"))
        )
        slow_type(email_field, email, delay=0.05)
        time.sleep(1)

        newsletter_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "styleApplied"))
        )
        newsletter_checkbox.click()
        time.sleep(1)

        abonare_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "_subscribe"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", abonare_btn)
        time.sleep(1)

        ActionChains(driver).move_to_element(abonare_btn).perform()

        driver.execute_script("""
            arguments[0].style.transition='0.3s';
            arguments[0].style.transform='scale(0.95)';
            arguments[0].style.backgroundColor='rgba(0,128,255,0.3)';
        """, abonare_btn)
        time.sleep(0.5)
        driver.execute_script("""
            arguments[0].style.transform='scale(1)';
            arguments[0].style.backgroundColor='';
        """, abonare_btn)

        time.sleep(3)

        logging.info("✅ Test finalizat cu succes !")

        time.sleep(3)

    except Exception as e:
        logging.error(f"❌ Eroare în execuție: {e}")

    finally:
        driver.quit()
        logging.info("🚪 Browser închis corect.")
