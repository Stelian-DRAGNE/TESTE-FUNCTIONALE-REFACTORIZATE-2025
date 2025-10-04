
"""

    2. Test acceptare cookie-uri pagină principală - Acest test acceptă politica de Cookie a site-ului ales pentru testare.

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


class PageTester:

    def __init__(
        self,
        driver_path: Optional[str] = None,
        headless: bool = True,
        request_timeout: int = 10,
        wait_timeout: int = 5,
    ) -> None:

        self.driver_path = driver_path
        self.headless = headless
        self.request_timeout = request_timeout
        self.wait_timeout = wait_timeout

    def _build_driver(self) -> webdriver.Chrome:

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(self.driver_path or ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _is_page_ok(self, url: str) -> bool:

        try:
            resp = requests.get(url, timeout=self.request_timeout)
            if resp.status_code == 200:
                logging.info("✔ Pagina %s este funcțională (200 OK).", url)
                return True
            logging.error("✖ Pagina NU este funcțională (status %s).", resp.status_code)
            return False
        except requests.RequestException as e:
            logging.error("Eroare la verificarea HTTP %s: %s", url, e)
            return False

    def _accept_cookies(self, driver: webdriver.Chrome) -> None:

        locators = [
            (By.ID, "__gomagCookiePolicy"),
            (By.CSS_SELECTOR, "#__gomagCookiePolicy button"),
            (By.XPATH, "//button[contains(text(),'Accept')]"),
        ]
        for by, selector in locators:
            try:
                btn = WebDriverWait(driver, self.wait_timeout).until(
                    EC.element_to_be_clickable((by, selector))
                )
                time.sleep(3)
                btn.click()
                logging.info("✔ Butonul de cookie-uri (%s='%s') a fost apăsat.", by, selector)
                return
            except Exception:
                continue
        logging.info("ℹ Nu am găsit butonul de cookie-uri (posibil deja acceptat/absent).")

    def test_page(self, url: str, view_time: int = 3) -> bool:

        if not self._is_page_ok(url):
            return False

        try:
            driver = self._build_driver()
            driver.maximize_window()
            driver.get(url)
            logging.info("✔ Pagina %s a fost deschisă în Chrome.", url)

            self._accept_cookies(driver)

            time.sleep(view_time)
            logging.info("✔ Testul paginii a reușit.")
            return True
        except Exception as e:
            logging.error("Eroare la deschiderea browserului pentru %s: %s", url, e)
            return False
        finally:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    url_to_test = "https://www.mosionroata.ro/"
    tester = PageTester(headless=False)  # schimbă în True pentru CI/CD
    success = tester.test_page(url_to_test, view_time=5)
    sys.exit(0 if success else 1)