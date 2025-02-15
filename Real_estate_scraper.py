import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd

start_time = time.time()
s = Service("D:/chrome_driver/chromedriver.exe")
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=s, options=chrome_options)


tytul = []
cena = []
pokoje = []
powierzchnia = []
piętro = []
miasto = []
dzielnica = []
ulica = []
opis = []
typ_budynku = []
rok_budowy = []
rynek = []
materiał_budowlany = []
liczba_sypialni = []
typ_kuchni = []
taras = []
stan_nieruchomości = []
balkon = []
ogrzewanie = []
liczba_pieter = []

driver.get("https://www.morizon.pl/mieszkania/gdynia/?ps%5Blocation%5D%5Bmap%5D=1&ps%5Blocation%5D%5Bmap_bounds%5D=54.5847367,18.5692156:54.422913,18.3577425&ps%5Bwith_price%5D=1&utm_source=google&utm_medium=cpc&utm_campaign=&utm_adgroup=&utm_term=&utm_placement=&gad_source=1&gclid=Cj0KCQiA_qG5BhDTARIsAA0UHSLckG3omu6Mopy88LSc_axGwb-HqzPb3qlUOeEEPfY1qxdUiZncwkMaArUyEALw_wcB&gclsrc=aw.ds")
input("Press enter to continue")
time.sleep(10)

def close_cookies_popup():
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[6]/button[2]"))
        )
        accept_button.click()
        print("Pop-up ciasteczek został zamknięty.")
    except (NoSuchElementException, TimeoutException):
        print("Brak pop-upu ciasteczek lub upłynął czas oczekiwania.")

close_cookies_popup()

def collect_links():
    driver.refresh()
    links = set()
    for link in driver.find_elements(By.CLASS_NAME, 'ROzmJ2'):
        url = link.get_attribute('href')
        if url:
            links.add(url)
    return links



def extract_listing_data(elements):

    data = {
        "Typ budynku": np.nan,
        "Rok budowy": np.nan,
        "Rynek": np.nan,
        "Materiał budowlany" : np.nan,
        "Liczba sypialni" : np.nan,
        "Typ kuchni": np.nan,
        "Taras": np.nan,
        "Stan nieruchomości" : np.nan,
        "Balkon": np.nan,
        "Ogrzewanie" : np.nan,
        "Liczba pięter" : np.nan,
        "Piętro" : np.nan
    }

    for element in elements:
        try:
            label_element = element.find_element(By.CLASS_NAME, "_3rio9t")
            value_element = element.find_element(By.CLASS_NAME, "M3ijI0")

            label = label_element.text.strip()
            value = value_element.text.strip()

            if label in data:
                data[label] = value

        except Exception as e:
            print(f"Error processing element: {e}")

    return data

def scrap_details():
    try:
        title = driver.find_element(By.CLASS_NAME, "cGImOq").text
        title = title.replace('\n',' ').replace(","," ")
    except NoSuchElementException:
        title = np.nan

    try:
        price = driver.find_element(By.CLASS_NAME, "mTbNh8").text
        price = str(price).replace("zł","").strip()
    except NoSuchElementException:
        price = np.nan

    try:
        flat_attributes = driver.find_elements(By.CLASS_NAME, "_1Aukq8")

        pokoje_text = np.nan
        powierzchnia_text = np.nan
        pietro_text = np.nan

        for attribute in flat_attributes:
            text = attribute.text.strip().lower()

            if "pok" in text:
                pokoje_text = text
            elif "m²" in text:
                powierzchnia_text = text
            elif "piętro" in text or "parter" in text:
                pietro_text = text
        pokoje_text=str(pokoje_text).replace("•", "").strip()
        powierzchnia_text = str(powierzchnia_text).replace("•", "").replace("m²", "").strip()

        pietro_text = str(pietro_text).replace("•", "").strip()

        pokoje.append(pokoje_text)
        powierzchnia.append(powierzchnia_text)
        piętro.append(pietro_text)

    except NoSuchElementException:
        print("Nie znaleziono elementów o podanej klasie '_1Aukq8'")

    try:
        location_elements = driver.find_elements(By.CLASS_NAME, "W-z1On")

        miasto_text = np.nan
        dzielnica_text = np.nan
        ulica_text = np.nan

        if location_elements:
            location_text = ", ".join([location.text.strip() for location in location_elements])
            parts = location_text.split(", ")

            miasto_text = parts[0] if len(parts) > 0 else np.nan
            dzielnica_text = parts[1] if len(parts) > 1 else np.nan
            ulica_text = parts[2] if len(parts) > 2 else np.nan
            miasto_text = str(miasto_text).replace(",","")
            dzielnica_text= str(dzielnica_text).replace(",","")
            ulica_text = str(ulica_text).replace(",","")

        miasto.append(miasto_text)
        dzielnica.append(dzielnica_text)
        ulica.append(ulica_text)

    except NoSuchElementException:
        print("Nie znaleziono elementów o podanej klasie 'W-z1On'")



    elements = driver.find_elements(By.CLASS_NAME, "iT04N1")
    additional_data = extract_listing_data(elements)

    try:
        read_more_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/main/div[4]/section/div[4]/button")
        read_more_button.click()
        time.sleep(2)
        desc = driver.find_element(By.CLASS_NAME, "Kyc-uW").text.strip()
        desc = desc.encode("utf-8", "ignore").decode("utf-8")
        desc = desc.replace("\n", " ").replace(",", " ").replace(";", " ")
    except NoSuchElementException:
        desc = np.nan
    except Exception as e:
        print(f"Problem z opisem: {e}")
        desc = np.nan


    tytul.append(title)
    cena.append(price)
    opis.append(desc)


    typ_budynku.append(additional_data["Typ budynku"])
    rok_budowy.append(additional_data["Rok budowy"])
    rynek.append(additional_data["Rynek"])
    materiał_budowlany.append(additional_data["Materiał budowlany"])
    liczba_sypialni.append(additional_data["Liczba sypialni"])
    typ_kuchni.append(additional_data["Typ kuchni"])
    taras.append(additional_data["Taras"])
    stan_nieruchomości.append(additional_data["Stan nieruchomości"])
    balkon.append(additional_data["Balkon"])
    ogrzewanie.append(additional_data["Ogrzewanie"])
    liczba_pieter.append(additional_data["Liczba pięter"])

def scroll_page():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def go_to_next_page(current_page, last_page):

    if current_page < last_page:
        next_page_url = f"https://www.morizon.pl/mieszkania/gdynia/?ps[location][map]=1&ps[location][map_bounds]=54.5847367,18.5692156:54.422913,18.3577425&ps[with_price]=1&page={current_page+1}&utm_source=google&utm_medium=cpc&utm_campaign=&utm_adgroup=&utm_term=&utm_placement=&gad_source=1&gclid=Cj0KCQiA_qG5BhDTARIsAA0UHSLckG3omu6Mopy88LSc_axGwb-HqzPb3qlUOeEEPfY1qxdUiZncwkMaArUyEALw_wcB&gclsrc=aw.ds"
        driver.get(next_page_url)
        print(f"Przechodzenie na stronę {current_page + 1}...")
        time.sleep(5)
        return True
    else:
        print("Osiągnięto ostatnią stronę.")
        return False



def navigate_links():
    all_links = set()
    current_page = 1


    last_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/main/div/section[2]/div[2]/div/div[2]/div[6]/a/div/span"))
    )
    last_page = int(last_page_element.text.strip())
    print(last_page)

    while True:
        print(f"Zbieranie linków z bieżącej strony {current_page}...")
        links = collect_links()
        all_links.update(links)

        print(f"Zebrano {len(links)} linków na stronie {current_page}. Łącznie unikalnych linków: {len(all_links)}")


        i = 1
        for link in links:
            print(f"Przechodzę na {i}/{len(links)}: {link}")
            driver.get(link)
            time.sleep(3)

            scrap_details()

            driver.back()
            time.sleep(2)
            i += 1


        if not go_to_next_page(current_page, last_page):
            print("Nie znaleziono kolejnej strony. Zakończono nawigację.")
            break

        current_page += 1

    print(f"Łącznie zebrano {len(all_links)} unikalnych linków.")

navigate_links()


data = {
    'Tytuł': tytul,
    'Cena': cena,
    'Pokoje': pokoje,
    'Powierzchnia': powierzchnia,
    'Piętro': piętro,
    'Miasto': miasto,
    'Dzielnica': dzielnica,
    'Ulica': ulica,
    'Typ budynku': typ_budynku,
    'Rok budowy': rok_budowy,
    'Rynek': rynek,
    'Materiał budowlany': materiał_budowlany,
    'Liczba sypialni': liczba_sypialni,
    'Typ kuchni': typ_kuchni,
    'Taras': taras,
    'Stan nieruchomości': stan_nieruchomości,
    'Balkon': balkon,
    'Ogrzewanie': ogrzewanie,
    'Liczba pięter': liczba_pieter,
    'Opis': opis
}
df = pd.DataFrame(data)
df.to_csv("D:/Morizon_scrapper/test/morizon_Gdynia_data1.csv", index=False, encoding="utf-8-sig")

end_time=time.time()
execution_time=end_time-start_time
print(execution_time)
