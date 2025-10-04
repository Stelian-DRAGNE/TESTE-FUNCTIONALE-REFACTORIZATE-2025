"""

    4.  Test accesare sectiunea 'DESPRE NOI'. 
        Acest test va accesa sectiunea 'DESPRE NOI', prezenta in cadrul site-ului ales pentru testare si completarea formularului online disponibil, urmata de simularea trimiterii formularului.

"""



import time
import logging
import os
from typing import Optional
from dotenv import load_dotenv
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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "4.despre_noi.env")
load_dotenv(dotenv_path=ENV_PATH)

FORM_DATA = {
    "nume": os.getenv("FORM_NUME", "Ion"),
    "prenume": os.getenv("FORM_PRENUME", "Popescu"),
    "email": os.getenv("FORM_EMAIL", "ion.popescu@test.ro"),
    "telefon": os.getenv("FORM_TELEFON", "0700000000"),
    "mesaj": os.getenv("FORM_MESAJ", "Acesta este un mesaj de test automat."),
}

CHAR_DELAY = 0.05  # 0.05s per caracter
FIELD_PAUSE = 1.0  # 1s pauză între câmpuri


def type_like_human(element, text: str, delay: float = CHAR_DELAY):
    for ch in text:
        element.send_keys(ch)
        time.sleep(delay)


def log_and_type(driver, field_name: str, value: str, mask: bool = True, pause: float = FIELD_PAUSE):
    elem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, field_name)))
    if mask:
        masked_value = "*" * len(value)
        type_like_human(elem, masked_value, delay=CHAR_DELAY)
    else:
        type_like_human(elem, value, delay=CHAR_DELAY)
    time.sleep(pause)


class WebFormTester:
    def __init__(self, driver_path: Optional[str] = None, headless: bool = False):
        self.driver_path = driver_path
        self.headless = headless

    def _build_driver(self) -> webdriver.Chrome:
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(self.driver_path or ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    def _scroll_page1_strict(self, driver, steps: int = 21, px: int = 200, delay: float = 1.0):
        driver.execute_script("document.documentElement.style.scrollBehavior='auto';")
        driver.execute_script("window.scrollTo(0,0)")
        for i in range(steps):
            driver.execute_script("window.scrollBy(0, arguments[0])", px)
            time.sleep(delay)

        final_y = steps * px
        driver.execute_script("window.scrollTo(0, arguments[0])", final_y)

        driver.execute_script("""
            (function(targetY){
                if (window.__scrollLockInstalled) return;
                window.__scrollLockInstalled = true;
                window.addEventListener('scroll', function(){
                    if (Math.abs(window.scrollY - targetY) > 1) {
                        window.scrollTo(0, targetY);
                    }
                }, {passive:true});
            })(arguments[0]);
        """, final_y)

    def _scroll_to_bottom(self, driver, px: int = 200, delay: float = 1.0):
        driver.execute_script("document.documentElement.style.scrollBehavior='auto';")
        driver.execute_script("window.scrollTo(0,0)")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, arguments[0])", px)
            time.sleep(delay)
            new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
            if new_height >= last_height:
                break

    def _scroll_steps(self, driver, steps: int, px: int = 200, delay: float = 1.0, label: str = "Pag2"):
        driver.execute_script("document.documentElement.style.scrollBehavior='auto';")
        driver.execute_script("window.scrollTo(0,0)")
        for i in range(steps):
            driver.execute_script("window.scrollBy(0, arguments[0])", px)
            time.sleep(delay)

    def _accept_cookies_page1(self, driver, wait: int = 5):
        try:
            btn = WebDriverWait(driver, wait).until(
                EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy"))
            )
            btn.click()
            logging.info("✅ Cookie acceptat (pagina 1).")
        except Exception:
            logging.info("ℹ️ Nu am găsit butonul de cookie (pagina 1).")

    def _open_page2(self, driver):
        old_tabs = driver.window_handles
        link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "AICI"))
        )
        time.sleep(2)
        driver.execute_script("arguments[0].click();", link)

        time.sleep(3)
        tabs_now = driver.window_handles
        if len(tabs_now) > len(old_tabs):
            driver.switch_to.window(tabs_now[-1])
        else:
            driver.switch_to.window(tabs_now[0])

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)

    def run_test(self, url: str) -> bool:
        driver = None
        try:
            driver = self._build_driver()
            driver.get(url)
            time.sleep(2)

            self._accept_cookies_page1(driver)
            time.sleep(2)
            self._scroll_page1_strict(driver, steps=21, px=200, delay=1.0)
            self._open_page2(driver)

            self._scroll_to_bottom(driver, px=200, delay=1.0)

            driver.execute_script("window.scrollTo(0,0)")
            time.sleep(1)

            self._scroll_steps(driver, steps=11, px=200, delay=1.0, label="Pag2")

            log_and_type(driver, "field[1]", FORM_DATA["nume"], mask=True)
            log_and_type(driver, "field[2]", FORM_DATA["prenume"], mask=True)
            log_and_type(driver, "field[0]", FORM_DATA["email"], mask=True)
            log_and_type(driver, "field[3]", FORM_DATA["telefon"], mask=True)
            log_and_type(driver, "field[4]", FORM_DATA["mesaj"], mask=False)

            checkbox = driver.find_element(By.XPATH, '//*[@id="__submit7"]/div/label/div/input')
            checkbox.click()

            driver.execute_script("window.scrollBy(0, 200)")
            time.sleep(2)

            trimite_btn = driver.find_element(By.ID, "__doSubmit7")
            driver.execute_script("arguments[0].style.border='3px solid red'", trimite_btn)
            time.sleep(2)
            logging.info("✅ Test finalizat.")
            return True

        except Exception as e:
            logging.error("❌ Eroare în test: %s", e)
            return False
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
                logging.info("🛑 Browser închis.")


if __name__ == "__main__":
    tester = WebFormTester(headless=False)
    success = tester.run_test("https://www.mosionroata.ro/")
    exit(0 if success else 1)
