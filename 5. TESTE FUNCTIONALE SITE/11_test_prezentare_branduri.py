
"""

    11. Test accesare sectiunea "BRANDURI"
        Acest test va prezenta lista brand-urilor comercializate de catre site-ul ales pentru testare, in ordinea numarului de pagini disponibile in acesta sectiune a site-ului.

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
        time.sleep(2)

    branduri_pagina_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/header/div[3]/nav/div/ul/li[5]/a'))
    )
    branduri_pagina_1.click()
    time.sleep(2)

    for _ in range(7):
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1.1)
    time.sleep(2)

    pagina_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#category-page > div.pagination.pg-categ.pull-right > ol > li:nth-child(2) > a"))
    )
    pagina_2.click()
    time.sleep(2)

    for _ in range(7):
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1.1)
    time.sleep(2)

    pagina_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#category-page > div.pagination.pg-categ.pull-right > ol > li:nth-child(4) > a"))
    )
    pagina_3.click()
    time.sleep(2)

    for _ in range(7):
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1.1)
    time.sleep(2)

    pagina_4 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#category-page > div.pagination.pg-categ.pull-right > ol > li:nth-child(5) > a"))
    )
    pagina_4.click()
    time.sleep(2)

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 200)")
        time.sleep(1.1)
    time.sleep(2)

    driver.get("https://www.mosionroata.ro/lista-marci")
    time.sleep(3)

    logging.info("✅ Test finalizat cu succes !")

except Exception as e:
    logging.error(f"❌ Eroare în test: {e}")

finally:
    driver.quit()
    logging.info("🚪 Browser închis corect.")
