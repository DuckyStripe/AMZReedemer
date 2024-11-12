import os
import zipfile
import requests
import threading
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import string
from datetime import datetime
import time
import random
import atexit
# Lista de User Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]
stop_event = threading.Event()
# URLs y rutas
CHROMEDRIVER_URL = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
DOWNLOAD_PATH = "chromedriver_linux64.zip"
CHROMEDRIVER_PATH = "./chromedriver"
COOKIES_FILE = "cookies.pkl"

class SessionManager:
    def __init__(self):
        self.driver = None
        self.cookies_file = "cookies.pkl"
        atexit.register(self.cleanup)  # Registrar función de limpieza

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            # Eliminar el navigator.webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except WebDriverException as e:
            print(f"Error al inicializar el navegador: {str(e)}")
            return False

    def save_cookies(self):
        if self.driver:
            try:
                cookies = self.driver.get_cookies()
                if cookies:
                    with open(self.cookies_file, "wb") as file:
                        pickle.dump(cookies, file)
                    print(f"Cookies guardadas exitosamente en {self.cookies_file}")
                    return True
                else:
                    print("No se encontraron cookies para guardar")
                    return False
            except Exception as e:
                print(f"Error al guardar cookies: {str(e)}")
                return False
        return False

    def check_redirect(self):
        """Verificar si se ha redirigido a la página de inicio de sesión."""
        if self.driver:
            current_url = self.driver.current_url
            return current_url == "https://www.amazon.com.mx/?ref_=nav_signin"
        return False

    def cleanup(self):
        """Limpieza al cerrar el script"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass

    def guardar_sesion(self):
        if not self.initialize_driver():
            print("No se pudo inicializar el navegador")
            return

        try:
            # Navegar a la página de inicio de sesión
            print("Navegando a la página de inicio de sesión...")
            self.driver.get("https://www.amazon.com.mx/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.mx%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=mxflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

            print("\nPor favor, inicia sesión manualmente en el navegador.")
            print("Esperando la redirección para guardar cookies...")

            while True:
                time.sleep(2)  # Reducir la carga del CPU
                if self.check_redirect():
                    print("\nRedirigido a la página de inicio de sesión correctamente.")
                    if self.save_cookies():
                        print("\nProceso completado exitosamente!")
                    break

        except KeyboardInterrupt:
            print("\nProceso interrumpido por el usuario")
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")
        finally:
            if os.path.exists(self.cookies_file) and os.path.getsize(self.cookies_file) == 0:
                os.remove(self.cookies_file)
                print("Archivo de cookies vacío eliminado")

def verificar_cookies():
    """Verifica si existen cookies guardadas y muestra solo la primera."""
    if os.path.exists(COOKIES_FILE):
        try:
            with open(COOKIES_FILE, 'rb') as file:
                cookies = pickle.load(file)
            if cookies:
                return cookies

            print("No se encontraron cookies para mostrar.")
            return None

        except Exception as e:
            print(f"Error al leer las cookies: {str(e)}")
            return None
    return None


def crear_driver_con_cookies(cookies):
    """Crea un nuevo driver con las cookies cargadas"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Primero navega a amazon.com.mx para poder establecer las cookies
    driver.get("https://www.amazon.com.mx")

    # Cargar las cookies
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Error al cargar cookie: {str(e)}")

    return driver

def descargar_chromedriver():
    print("Descargando ChromeDriver...")
    response = requests.get(CHROMEDRIVER_URL)
    with open(DOWNLOAD_PATH, 'wb') as file:
        file.write(response.content)
    print("Descarga completa.")

def descomprimir_chromedriver():
    print("Descomprimiendo ChromeDriver...")
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        zip_ref.extractall(".")
    print("Descompresión completa.")
    os.chmod(CHROMEDRIVER_PATH, 0o755)

def validar_y_configurar_chromedriver():
    if not os.path.exists(CHROMEDRIVER_PATH):
        descargar_chromedriver()
        descomprimir_chromedriver()
    else:
        print("ChromeDriver ya está disponible en la ruta especificada.")
def generar_combo(base_pattern):
    if '?' not in base_pattern:
        # No hay caracteres '?' en el patrón, así que solo devolvemos el patrón tal cual.
        return [base_pattern]

    caracteres_validos = string.ascii_uppercase + string.digits
    posibles_cadenas = []
    for char in caracteres_validos:
        nueva_cadena = base_pattern.replace('?', char)
        posibles_cadenas.append(nueva_cadena)
    return posibles_cadenas

def espera_aleatoria():
    tiempo_espera = random.uniform(20, 50)
    print(f"Esperando {tiempo_espera:.2f} segundos antes del siguiente intento...")
    time.sleep(tiempo_espera)
def probar_codigo(driver, codigo, intento, tarjeta):

    # Comprobar mensajes de error
    fecha_actual = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"resultados_{tarjeta}_{fecha_actual}.txt"
    separador = "="*40
    while not stop_event.is_set():
        try:
            print(f"\nIntento #{intento}")
            print(f"Probando código: {codigo}")

            # Esperar a que el campo de entrada esté presente
            gift_card_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "gc-redemption-input"))
            )

            # Limpiar el campo de entrada y escribir el código
            gift_card_input.clear()
            for letra in codigo:
                gift_card_input.send_keys(letra)
                time.sleep(random.uniform(0.1, 0.3))

            # Hacer clic en el botón de canje
            redeem_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "gc-redemption-apply-button"))
            )
            redeem_button.click()

            # Breve pausa para permitir que el mensaje aparezca
            time.sleep(2)

            try:
                error_msg = driver.find_element(By.ID, "gc-redemption-error")
                if error_msg.is_displayed():
                    mensaje_error = error_msg.text
                    salida = f"Código {codigo}: No válido. Mensaje de error: {mensaje_error}"

                    if "Ya fue canjeado en otra cuenta" in mensaje_error:
                        salida = f"Código {codigo}: Ya se canjeó la tarjeta. Proceso detenido."
                        print(salida)
                        with open(nombre_archivo, "a") as file:
                            file.write("\n" + salida + "\n" + separador)
                        stop_event.set()  # Detener todos los hilos
                        return

                    print(salida)
                    with open(nombre_archivo, "a") as file:
                        file.write("\n" + salida + "\n" + separador)
                    break
            except:
                pass

            # Comprobar mensajes de éxito u otras informaciones
            try:
                info_msg = driver.find_element(By.ID, "gc-redemption-info-message")
                if info_msg.is_displayed():
                    salida = f"Código {codigo}: Información adicional. Mensaje: {info_msg.text}"
                    print(salida)
                    with open(nombre_archivo, "a") as file:
                        file.write("\n" + salida + "\n" + separador)
                    break
            except:
                pass

            salida = f"Código {codigo}: No se encontró mensaje de error conocido."
            print(salida)
            with open(nombre_archivo, "a") as file:
                file.write("\n" + salida + "\n" + separador)
            break

        except WebDriverException as e:
            salida = f"Error al probar el código {codigo}: {str(e)}. Reintentando debido a una redirección inesperada..."
            print(salida)
            with open(nombre_archivo, "a") as file:
                file.write("\n" + salida + "\n" + separador)
            espera_aleatoria()

        except Exception as e:
            salida = f"Error inesperado al probar el código {codigo}: {str(e)}"
            print(salida)
            with open(nombre_archivo, "a") as file:
                file.write("\n" + salida + "\n" + separador)
            time.sleep(random.uniform(120, 180))
            break


def ejecutar_pruebas_con_hilos(posibles_cadenas, tarjeta,hilos):
    max_hilos = hilos
    threads = []

    def crear_y_probar_codigo(codigo, intento):
        cookies = verificar_cookies()
        driver = crear_driver_con_cookies(cookies)
        try:
            driver.get("https://www.amazon.com.mx/gc/redeem")
            probar_codigo(driver, codigo, intento, tarjeta)
        finally:
            driver.quit()

    for i, codigo in enumerate(posibles_cadenas, 1):
        if stop_event.is_set():
            break  # Detener creación de nuevos hilos si el evento está activado

        # Se crea un hilo nuevo para cada código
        thread = threading.Thread(target=crear_y_probar_codigo, args=(codigo, i))
        threads.append(thread)
        thread.start()

        # Limitar número de hilos simultáneos
        if len(threads) >= max_hilos:
            for thread in threads:
                thread.join()  # Esperar a que terminen los hilos actuales
            threads = []  # Reiniciar lista de hilos

    # Asegurarse de que todos los hilos terminen
    for thread in threads:
        thread.join()

def manejar_interrupcion():
    """Maneja la interrupción del usuario (Ctrl+C) y pregunta sobre las cookies."""
    respuesta = input("¿Desea conservar las cookies guardadas? (s/n): ").strip().lower()
    if respuesta == 'n':
        try:
            if os.path.exists(COOKIES_FILE):
                os.remove(COOKIES_FILE)
                print("Cookies eliminadas.")
            else:
                print("No hay cookies para eliminar.")
        except Exception as e:
            print(f"Error al eliminar las cookies: {str(e)}")
    else:
        print("Cookies conservadas.")

def main():
    print("=" * 40)
    print(" Bienvenido al Verificador de Gift Cards ")
    print("=" * 40)
    print("Validando Cookies....")

    # Primero verificar si existen cookies
    cookies = verificar_cookies()
    print("=" * 40)

    if not cookies:
        print("No se encontraron cookies guardadas. Iniciando proceso de login...")
        session_manager = SessionManager()

        try:
            session_manager.guardar_sesion()
            # Después de guardar la sesión, volver a verificar las cookies
            cookies = verificar_cookies()
        except Exception as e:
            print(f"Error al guardar la sesión: {str(e)}")
            return

    if not cookies:
        print("No se pudieron obtener las cookies. Saliendo...")
        return

    # Configurar ChromeDriver
    validar_y_configurar_chromedriver()

    # Solicitar al usuario que ingrese el patrón de la tarjeta
    try:
        tarjeta = input("Introduce el patrón de la tarjeta (usa ? para el carácter desconocido): ")
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Saliendo del programa...")
        manejar_interrupcion()
        return

    posibles_cadenas = generar_combo(tarjeta)
    print(f"Se generaron {len(posibles_cadenas)} combinaciones posibles.")
    try:
        if posibles_cadenas == 1:
            ejecutar_pruebas_con_hilos(posibles_cadenas,tarjeta,1)
        else:
            ejecutar_pruebas_con_hilos(posibles_cadenas,tarjeta,5)

    except KeyboardInterrupt:
        print("\n\nInterrupción detectada. Finalizando proceso...")
        manejar_interrupcion()

    except Exception as e:
        print("=" * 40)
        print(f"Error general: {str(e)}")

    finally:
        print("=" * 40)
        print("\nProceso finalizado.")
        exit

if __name__ == "__main__":
    main()

