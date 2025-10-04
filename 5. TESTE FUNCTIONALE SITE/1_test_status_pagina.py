
"""

    1. Test verificare status pagină principală - Acest test va verifica dacă pagina principală a site-ului ales pentru testare este activă și nu returnează un cod de eroare, cel pregonizat fiind 200.

"""



import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def check_and_open_page(url: str, headless: bool = False, wait_time: int = 3) -> bool:

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            logging.error("Pagina NU este funcțională (status %s).", resp.status_code)
            return False
        logging.info("✔ Pagina %s este funcțională (200 OK).", url)
    except requests.RequestException as e:
        logging.error("Eroare la verificarea %s: %s", url, e)
        return False

    try:
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(), options=options)
        driver.maximize_window()
        driver.get(url)
        logging.info("Pagina s-a deschis în Chrome.")
        time.sleep(wait_time)
        driver.quit()
        logging.info("Test reușit ✅. Browser închis.")
        return True
    except Exception as e:
        logging.error("Eroare la deschiderea paginii în Chrome: %s", e)
        return False


if __name__ == "__main__":
    url = "https://www.mosionroata.ro/"
    ok = check_and_open_page(url, headless=False, wait_time=5)
    exit(0 if ok else 1)
