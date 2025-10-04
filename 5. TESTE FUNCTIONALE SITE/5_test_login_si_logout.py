
"""

    5. Test "Intra pe cont" pe site – Acest test va simula crearea unui cont utilizator/client fara a se transmite solicitarea. Se va continua cu logarea în cont de utilizator/client creat în prealabil, verificare a uneia dintre secțiunile disponibile, și apoi 'Logout'.

"""



import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "5_test_login_si_logout.env")
load_dotenv(dotenv_path=ENV_PATH)


LOGIN_EMAIL = os.getenv("USER_EMAIL")
LOGIN_PASSWORD = os.getenv("USER_PASSWORD")

PROFILE_EMAIL = os.getenv("PROFILE_EMAIL", "new_email@test.ro")
PROFILE_LASTNAME = os.getenv("PROFILE_LASTNAME", "NumeNou")
PROFILE_FIRSTNAME = os.getenv("PROFILE_FIRSTNAME", "PrenumeNou")
PROFILE_PHONE = os.getenv("PROFILE_PHONE", "0712345678")


if not LOGIN_EMAIL or not LOGIN_PASSWORD:
    raise ValueError("❌ USER_EMAIL și USER_PASSWORD lipsesc din .env!")


CHAR_DELAY = 0.05    
FIELD_PAUSE = 1.0   
POST_ACTION_PAUSE = 2 


def safe_click(driver, by, selector, timeout=10):
    elem = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
    driver.execute_script("arguments[0].click();", elem)
    return elem


def safe_type(driver, by, selector, value, mask=False, delay=CHAR_DELAY, pause=FIELD_PAUSE, timeout=10):
    elem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
    elem.clear()
    for ch in value:
        elem.send_keys(ch)
        time.sleep(delay)
    log_val = "*" * len(value) if mask else value
    time.sleep(pause)
    return elem


def type_fake_stars(driver, by, selector, length, delay=CHAR_DELAY, pause=FIELD_PAUSE, timeout=10):
    fake_value = "*" * length
    elem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))
    elem.clear()
    for ch in fake_value:
        elem.send_keys(ch)
        time.sleep(delay)
    time.sleep(pause)
    return elem


def simulate_register(driver):
    safe_click(driver, By.XPATH, '//*[@id="wrapper"]/header/div[2]/div/div/div[3]/ul/li[2]/a/i')
    time.sleep(POST_ACTION_PAUSE)

    safe_click(driver, By.ID, "doRegister")
    time.sleep(1)

    type_fake_stars(driver, By.ID, "__emailRegister", 24)
    type_fake_stars(driver, By.ID, "__lastnameRegister", 6)
    type_fake_stars(driver, By.ID, "__firstnameRegister", 7)
    type_fake_stars(driver, By.ID, "__passwordRegister", 12)
    type_fake_stars(driver, By.ID, "__confirmPasswordRegister", 12)

    safe_click(driver, By.NAME, "agreeNewsletterInformation")
    time.sleep(1)
    safe_click(driver, By.NAME, "agreePersonalInformation")
    time.sleep(1)

    reg_btn = driver.find_element(By.ID, "doRegister")
    driver.execute_script("arguments[0].style.border='3px solid red'", reg_btn)
    time.sleep(POST_ACTION_PAUSE)

    driver.refresh()
    time.sleep(POST_ACTION_PAUSE)


def perform_login(driver, email, password):
    safe_click(driver, By.XPATH, '//*[@id="wrapper"]/header/div[2]/div/div/div[3]/ul/li[2]/a/i')
    time.sleep(POST_ACTION_PAUSE)

    safe_type(driver, By.ID, "_loginEmail", email, mask=False)      
    safe_type(driver, By.ID, "_loginPassword", password, mask=True)  

    time.sleep(POST_ACTION_PAUSE)  
    safe_click(driver, By.ID, "doLogin")
    time.sleep(POST_ACTION_PAUSE) 


def update_personal_data(driver):
    safe_click(driver, By.LINK_TEXT, "Date Personale")
    time.sleep(POST_ACTION_PAUSE)

    safe_type(driver, By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[2]/form/div[1]/input', PROFILE_EMAIL, mask=False)
    safe_type(driver, By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[2]/form/div[2]/input', PROFILE_LASTNAME, mask=False)
    safe_type(driver, By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[2]/form/div[3]/input', PROFILE_FIRSTNAME, mask=False)
    safe_type(driver, By.XPATH, '//*[@id="wrapper"]/div[4]/div/div[2]/form/div[4]/input', PROFILE_PHONE, mask=False)

    driver.execute_script("sessionStorage.setItem('scrollY', window.scrollY);")

    safe_click(driver, By.ID, "doSave")
    time.sleep(POST_ACTION_PAUSE)

    driver.execute_script("""
        const y = sessionStorage.getItem('scrollY');
        if (y) { window.scrollTo(0, y); }
    """)
    time.sleep(1.5)

    try:
        confirm_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert"))
        )
    except Exception:
        logging.warning("⚠️ Nu am găsit mesaj de confirmare.")

    safe_click(driver, By.LINK_TEXT, "Logout")
    time.sleep(POST_ACTION_PAUSE)


if __name__ == "__main__":
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get("https://www.mosionroata.ro/")
        time.sleep(POST_ACTION_PAUSE)

        try:
            cookie_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "__gomagCookiePolicy"))
            )
            driver.execute_script("arguments[0].click();", cookie_btn)
            time.sleep(3)
            time.sleep(POST_ACTION_PAUSE)
        except Exception:
            logging.info("ℹ️ Cookie nu a apărut (posibil deja acceptat).")

        simulate_register(driver)
        perform_login(driver, LOGIN_EMAIL, LOGIN_PASSWORD)
        update_personal_data(driver)

    finally:
        driver.quit()
        logging.info(" ✅ Testul a reusit.")
        logging.info("🚪 Browser închis.")
