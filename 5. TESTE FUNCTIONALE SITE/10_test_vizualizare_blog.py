
"""

    10. Test accesare sectiunea 'BLOG'.
        Acest test va efectua accesarea sectiunii "BLOG", sectiune prezenta in cadrul site-ului ales pentru testare.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


options = Options()
options.add_argument("--disable-search-engine-choice-screen")
service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()


try:
    driver.get("https://www.mosionroata.ro/")
    time.sleep(2)

    try:
        cookie_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy")))
        cookie_btn.click()
    except Exception:
        logging.info("ℹ️ Butonul de cookie nu a fost găsit (probabil deja acceptat).")
    time.sleep(2)

    blog_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div[3]/nav/div/ul/li[4]/a"))
    )
    blog_link.click()
    time.sleep(3)

    stopScrolling = 0
    while True:
        stopScrolling += 1
        driver.execute_script("window.scrollBy(0, 200)")
        if stopScrolling > 15:
            break
        time.sleep(1.1)
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(2)

    stopScrolling = 0
    while True:
        stopScrolling += 1
        driver.execute_script("window.scrollBy(0, 200)")
        if stopScrolling > 9:
            break
        time.sleep(1.1)
    time.sleep(2)

    driver.get("https://www.mosionroata.ro/blog/cum-sa-reglezi-corect-casca-pentru-copil.html")
    time.sleep(3)

    stopScrolling = 0
    while True:
        stopScrolling += 1
        driver.execute_script("window.scrollBy(0, 200)")
        if stopScrolling > 21:
            break
        time.sleep(1.1)
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(3)

    logging.info("✅ Test finalizat cu succes!")

except Exception as e:
    logging.error(f"❌ Eroare în test: {e}")

finally:
    driver.quit()
    logging.info("🚪 Browser închis corect.")
