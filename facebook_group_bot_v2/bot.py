import os
import time
import itertools
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

class FacebookAutoPosterSelenium:
    """Publica contenido en grupos de Facebook usando Selenium."""

    def __init__(self, credentials, group_ids, json_url):
        self.credentials = credentials
        self.group_ids = group_ids
        self.json_url = json_url
        self.cred_cycle = itertools.cycle(self.credentials)

    def fetch_content(self):
        try:
            resp = requests.get(self.json_url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"Error al obtener contenido: {exc}")
            return None

    def login(self, driver, email, password):
        driver.get("https://www.facebook.com/login")
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        pass_input = driver.find_element(By.ID, "pass")
        email_input.send_keys(email)
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        WebDriverWait(driver, 15).until(EC.url_contains("facebook.com"))

    def post_to_group(self, group_id, message, link=None):
        email, password = next(self.cred_cycle)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        try:
            self.login(driver, email, password)
            driver.get(f"https://www.facebook.com/groups/{group_id}")
            box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[role='textbox']"))
            )
            box.click()
            box.send_keys(message)
            if link:
                box.send_keys(" " + link)
            time.sleep(2)
            post_button = driver.find_element(By.XPATH, "//div[@aria-label='Publicar']")
            post_button.click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Se publicó')]"))
            )
            print(f"Publicado en {group_id} con {email}")
        except Exception as exc:
            print(f"Error al publicar en {group_id}: {exc}")
        finally:
            driver.quit()

    def autopost(self):
        content = self.fetch_content()
        if not content:
            print("No hay contenido para publicar")
            return []
        message = content.get("message")
        link = content.get("link")
        for group_id in self.group_ids:
            self.post_to_group(group_id, message, link)

if __name__ == "__main__":
    creds_env = os.getenv("FB_CREDENTIALS", "")
    group_ids = os.getenv("GROUP_IDS", "").split(",")
    json_url = os.getenv("JSON_URL", "")

    credentials = []
    for cred in creds_env.split(','):
        if ':' in cred:
            email, password = cred.split(':', 1)
            credentials.append((email.strip(), password.strip()))
    group_ids = [g.strip() for g in group_ids if g.strip()]

    if not credentials or not group_ids or not json_url:
        print("Debes definir FB_CREDENTIALS, GROUP_IDS y JSON_URL en las variables de entorno")
        exit(1)

    poster = FacebookAutoPosterSelenium(credentials, group_ids, json_url)
    poster.autopost()
