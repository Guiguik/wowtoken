import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def get_wow_token_price(region: str = "eu") -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://wowtoken.app/")
        wait = WebDriverWait(driver, 15)
        #selecteur token us pour comparaison
        price_element = wait.until(EC.presence_of_element_located((By.ID, "token")))
        price_us = price_element.text.strip()
        # Sélecteur du menu
        select_element = wait.until(EC.presence_of_element_located((By.ID, "region")))
        select = Select(select_element)
        time.sleep(2)
        # Sélectionner la région souhaitée
        select.select_by_value(region)
        time.sleep(10)  # attendre un peu que JS mette à jour la page

        # Vérifier que la région sélectionnée est bien celle qu'on veut
        selected = select.first_selected_option.get_attribute("value")
        if selected != region:
            print(f"⚠️ Erreur de sélection, région lue : {selected}")
            return "Région incorrecte"

        # Attendre que le prix soit bien mis à jour
        price_element = wait.until(EC.presence_of_element_located((By.ID, "token")))
        price = price_element.text.strip()

        return price

    except Exception as e:
        print(f"Erreur récupération prix ({region}) : {e}")
        return "N/A"
    finally:
        driver.quit()
