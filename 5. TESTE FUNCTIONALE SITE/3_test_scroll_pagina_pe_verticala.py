"""

    3.  Test scroll pe verticală pagină principală - Acest test va face scroll pe verticală a paginii principale a site-ului ales pentru testare.

"""



import logging
import sys
import time
from typing import Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


class PageScroller:

    def __init__(
        self,
        driver_path: Optional[str] = None,
        headless: bool = True,
        request_timeout: int = 10,
    ) -> None:
        self.driver_path = driver_path
        self.headless = headless
        self.request_timeout = request_timeout

    def _is_page_ok(self, url: str) -> bool:

        try:
            resp = requests.get(url, timeout=self.request_timeout)
            if resp.status_code == 200:
                logging.info("✅ Pagina %s este funcțională (200 OK).", url)
                return True
            logging.error("❌ Pagina NU este funcțională (status %s).", resp.status_code)
            return False
        except requests.RequestException as e:
            logging.error("❌ Eroare la verificarea paginii %s: %s", url, e)
            return False

    def _build_driver(self) -> webdriver.Chrome:

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(self.driver_path or ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _accept_cookies(self, driver: webdriver.Chrome, wait_cookie: int) -> None:

        try:
            cookie_button = WebDriverWait(driver, wait_cookie).until(
                EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy"))
            )
            cookie_button.click()
            logging.info("✅ Butonul de cookie-uri a fost apăsat.")
        except Exception:
            logging.info("ℹ️ Nu am găsit butonul de cookie-uri (posibil deja acceptat/absent).")
        time.sleep(2)

    def _do_scroll(
        self,
        driver: webdriver.Chrome,
        scroll_steps: int,
        scroll_px: int,
        scroll_delay: float,
    ) -> None:

        for step in range(1, scroll_steps + 1):
            driver.execute_script(f"window.scrollBy(0, {scroll_px})")
            time.sleep(scroll_delay)

    def scroll_page(
        self,
        url: str,
        scroll_steps: int = 30,
        scroll_px: int = 200,
        scroll_delay: float = 1.0,  
        wait_load: int = 3,
        wait_cookie: int = 5,
    ) -> bool:

        if not self._is_page_ok(url):
            return False

        driver = None
        try:
            driver = self._build_driver()
            driver.maximize_window()
            driver.get(url)
            time.sleep(wait_load)

            self._accept_cookies(driver, wait_cookie)

            self._do_scroll(driver, scroll_steps, scroll_px, scroll_delay)

            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(wait_load)
            logging.info("✅ Testul de scroll a reușit.")
            return True
        except Exception as e:
            logging.error("❌ Eroare la rularea browserului pentru %s: %s", url, e)
            return False
        finally:
            if driver:
                driver.quit()
                logging.info("🛑 Browser-ul a fost închis.")


if __name__ == "__main__":
    url_to_test = "https://www.mosionroata.ro/"
    scroller = PageScroller(headless=False)  
    success = scroller.scroll_page(
        url_to_test,
        scroll_steps=30,  
        scroll_px=200,     
        scroll_delay=1.0,  
        wait_load=3,
        wait_cookie=5,
    )
    sys.exit(0 if success else 1)
