
"""

    9.  Test sortare 'Biciclete Mountainbike' din secțiunea 'TOATE PRODUSELE' - Acest test va efectua sortarea produselor 'Biciclete Mountainbike' din secțiunea "TOATE PRODUSELE", în urma aplicării filtrelor dorite, disponibile pe pagina 'Biciclete Mountainbike'.

"""



import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


def aplica_filtru(driver, xpath, descriere):
    el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    el.click()
    time.sleep(1.5)
    driver.execute_script("window.scrollBy(0,300);")
    time.sleep(1)


options = Options()
options.add_argument("--disable-search-engine-choice-screen")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

try:
    driver.get("https://www.mosionroata.ro/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)

    try:
        cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy")))
        cookie.click()
    except Exception:
        logging.info("ℹ️ Cookie deja acceptat sau elementul nu este prezent.")
    time.sleep(2)

    hover = ActionChains(driver)
    biciclete = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#main-menu > div > ul > li.all-product-button.menu-drop > div > ul > li:nth-child(1) > a > i")
        )
    )
    hover.move_to_element(biciclete).perform()
    time.sleep(1)

    biciclete_mountainbike = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#main-menu > div > ul > li.all-product-button.menu-drop > div > ul > li:nth-child(1) > ul > li:nth-child(2) > div > p > a')
        )
    )
    hover.move_to_element(biciclete_mountainbike).perform()
    biciclete_mountainbike.click()
    time.sleep(3)

    driver.execute_script("window.scrollBy(0,350);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[2]/ul/li[4]/label/div', "Producător: Rock Machine")

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[4]/ul/li[2]/label/div', "Gen: Unisex") 

    driver.execute_script("window.scrollBy(0,400);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[5]/ul/li/label/div', "Diametru roți: 29 inch")

    driver.execute_script("window.scrollBy(0,450);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[6]/ul/li/label/div', "Material: Aluminiu")

    driver.execute_script("window.scrollBy(0,500);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[7]/ul/li[2]/label/div', "Viteze: 18 viteze")
    
    driver.execute_script("window.scrollBy(0,550);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[8]/ul/li/label/div', "Furcă: Cu suspensie")

    driver.execute_script("window.scrollBy(0,600);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[9]/ul/li/label/div', "Suspensie spate: Nu")

    driver.execute_script("window.scrollBy(0,650);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[10]/ul/li/label/div', "Frânare: Disc hidraulic")

    driver.execute_script("window.scrollBy(0,700);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[11]/ul/li[1]/label/div', "Culoare: Negru")

    driver.execute_script("window.scrollBy(0,800);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[12]/ul/li[5]/label/div', "Mărime cadru: 58cm")

    driver.execute_script("window.scrollBy(0,950);")
    time.sleep(3)

    aplica_filtru(driver, '/html/body/div[3]/div[4]/div/div[2]/div/div[13]/ul/li[2]/label/div', "Stoc: Magazin")


    driver.execute_script("window.scrollTo(0,475);")
    time.sleep(3)

    vezi_variante = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="category-page"]/div/div[3]/div[3]/div/div/div/div[2]/div[2]/div[1]/a/span'))
    )
    vezi_variante.click()
    time.sleep(3)

    driver.execute_script("window.scrollTo(0,200);")
    time.sleep(3)

    logging.info("✅ Testul de sortare 'Biciclete Mountainbike' a fost realizat cu succes.")


except Exception as e:
    logging.error(f"❌ Eroare în test: {e}")

finally:
    driver.quit()
    logging.info("🚪 Browser închis corect.")
