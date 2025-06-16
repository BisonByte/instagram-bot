from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from typing import List, Tuple

load_dotenv()

USUARIO = os.getenv("USUARIO")
CONTRASENA = os.getenv("CONTRASENA")
PROXY = os.getenv("PROXY")
TIEMPO_MAX_CARGA = 20
TIEMPO_MIN_CARGA = 2


def cargar_credenciales(file_path: str = "credentials.txt") -> List[Tuple[str, str]]:
    """Carga múltiples cuentas desde un archivo de texto."""
    credenciales: List[Tuple[str, str]] = []
    if not os.path.exists(file_path):
        return credenciales

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            linea = line.strip()
            if not linea or linea.startswith("#"):
                continue
            if ":" in linea:
                usuario, clave = linea.split(":", 1)
            elif "," in linea:
                usuario, clave = linea.split(",", 1)
            else:
                continue
            credenciales.append((usuario.strip(), clave.strip()))

    return credenciales

xpath = {
   "decline_cookies": "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]",
    "save_login_not_now_button": "//div[contains(text(), 'Ahora no')]",
    "notification_not_now_button": "//button[contains(text(), 'Ahora no')]",
    "like_button": "//*[@aria-label='Me gusta']",
    "modal": "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]",
    "cancel_unfollow_button": "//button[contains(text(), 'Cancel')]",
}

css_selector = {
    "follows_buttons": "._aano button"
}

urls = {
    "login": "https://www.instagram.com/accounts/login/",
    "post": "https://www.instagram.com/p/CzZQt6BIsck/"
}


class SeguidorInstagram:

    def __init__(self, usuario: str, clave: str):
        self.usuario = usuario
        self.clave = clave
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        if PROXY:
            chrome_options.add_argument(f"--proxy-server={PROXY}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def cerrar_navegador(self):
        self.driver.close()

    def iniciar_sesion(self):
        self.driver.get(urls["login"])

        try:
            cookie_warning = WebDriverWait(self.driver, TIEMPO_MIN_CARGA).until(
                EC.presence_of_element_located((By.XPATH, xpath["decline_cookies"]))
            )
            # Cierra la advertencia de cookies haciendo clic en el elemento
            cookie_warning[0].click()
        except:
            pass

        username_input = self.driver.find_element(by=By.NAME, value="username")
        password_input = self.driver.find_element(by=By.NAME, value="password")

        username_input.send_keys(self.usuario)
        password_input.send_keys(self.clave)

        WebDriverWait(self.driver, TIEMPO_MIN_CARGA)
        password_input.send_keys(Keys.ENTER)

        try:
            # Pulsa "Ahora no" e ignora la ventana de guardar inicio
            save_login_prompt = WebDriverWait(self.driver, TIEMPO_MIN_CARGA).until(
                EC.presence_of_element_located((By.XPATH, xpath["save_login_not_now_button"]))
            )
            save_login_prompt.click()
        except:
            pass

        try:
            # Pulsa "Ahora no" en la notificación de avisos
            notifications_prompt = WebDriverWait(self.driver, TIEMPO_MIN_CARGA).until(
                EC.presence_of_element_located((By.XPATH, xpath["notification_not_now_button"]))
            )
            notifications_prompt.click()
        except:
            pass

    def dar_like_publicacion(self):
        self.driver.get(xpath["post"])

        # Dar like
        like_button = WebDriverWait(self.driver, TIEMPO_MAX_CARGA).until(
        EC.element_to_be_clickable((By.XPATH, xpath["like_button"]))
        )
        like_button.click()
        print("Like dado")
    
    def encontrar_seguidores(self, nombre_cuenta):
        WebDriverWait(self.driver, TIEMPO_MIN_CARGA)

        # Mostrar seguidores de la cuenta seleccionada.
        self.driver.get(f"https://www.instagram.com/{nombre_cuenta}/followers/")

        # El xpath del modal que muestra los seguidores puede cambiar con el tiempo. Actualízalo si es necesario.
        modal = WebDriverWait(self.driver, TIEMPO_MAX_CARGA).until(
            EC.presence_of_element_located((By.XPATH, xpath["modal"]))
        )
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            WebDriverWait(self.driver, TIEMPO_MIN_CARGA)
  

    def seguir(self):
        # Verifica y actualiza el selector de los botones "Seguir" si es necesario.
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, value=css_selector["follows_buttons"])

        for button in all_buttons:
            try:
                button.click()
                WebDriverWait(self.driver, TIEMPO_MIN_CARGA)

            # Al hacer clic en alguien que ya sigues se abrirá el diálogo para dejar de seguir/Cancelar
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value=xpath["cancel_unfollow_button"])
                cancel_button.click()     

if __name__ == "__main__":
    credenciales = cargar_credenciales()
    if not credenciales and USUARIO and CONTRASENA:
        credenciales = [(USUARIO, CONTRASENA)]

    for usuario, clave in credenciales:
        bot = SeguidorInstagram(usuario, clave)
        bot.iniciar_sesion()
        bot.encontrar_seguidores("leomessi")
        bot.cerrar_navegador()
