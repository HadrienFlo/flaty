import json
from dataclasses import dataclass

# import httpx
# from selectolax.parser import HTMLParser
# from rich import print


# imports to manage cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class Site:
    name: str
    url: str
    search_url: str
    cookie_button_getter: str
    ad_url_getter: str
    ad_price_getter: str
    ad_keyfacts_getter: str
    ad_location_getter: str
    ad_img_getter: str


@dataclass
class Ad:
    site: Site
    url: str
    price: str
    keyfacts: list[str]
    location: str
    img: str


def load_sites(urls: dict[str, str]) -> list[Site]:
    with open("src/sites.json", "r") as f:
        data = json.load(f)
    for item in data:
        item["search_url"] = urls.get(item["name"], "")
    return [Site(**item) for item in data]


# def load_page(client, url):
#     response = client.get(url)
#     return HTMLParser(response.text)


# def to_xpath(css_selector: str) -> str:
#     steps = css_selector.split(">")
#     for step in steps:
#         select = step.split(", ")
#         xpath_strings = [selector.split(".")[1] for selector in select]
#         # tag1[@attr1='value1' or @attr]
#         xpath_step = "//%s[%s]" % (select[0].split(".")[0], " or ".join([f"@class='{xpath_string}'" for xpath_string in xpath_strings]))
#     selectors = css_selector.split(", ")
#     xpath_strings = [selector.split(".")[1] for selector in selectors]
#     xpath = "//%s[%s]" % (selectors[0].split(".")[0], " or ".join([f"@class='{xpath_string}'" for xpath_string in xpath_strings]))
#     print(xpath)
#     return xpath


def parse(driver: webdriver, site: Site):
    url_list = driver.find_elements(By.XPATH, site.ad_url_getter)
    price_list = driver.find_elements(By.XPATH, site.ad_price_getter)
    keyfacts_list = driver.find_elements(By.XPATH, site.ad_keyfacts_getter)
    location_list = driver.find_elements(By.XPATH, site.ad_location_getter)
    img_list = driver.find_elements(By.XPATH, site.ad_img_getter)
    Ads = [
        Ad(
            site=site,
            url=url.get_attribute('href'),
            price=price.text.strip(),
            keyfacts=keyfacts.text.strip(),
            location=location.text.strip(),
            img=img.get_attribute('src')
        )
        for url, price, keyfacts, location, img in zip(url_list, price_list, keyfacts_list, location_list, img_list)
    ]
    return Ads


def main():
    urls = {
        "SeLoger": "https://www.seloger.com/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations=AD08FR31096&numberOfBedroomsMin=1&numberOfRoomsMin=1&priceMax=1200&spaceMin=30",
        "PAP": "https://www.pap.fr/annonce/locations-paris-75-g439-a-partir-du-2-pieces-jusqu-a-800-euros-a-partir-de-15-m2",
        "Bien'ici": "https://www.bienici.com/recherche/location/paris-5-75/appartement?prixMax=800&surfaceMin=15&nbPiecesMin=1"
    }
    print("Starting")
    
    print("Loading sites")
    sites = load_sites(urls)[:2]

    print(f"Sites loaded")
    print(sites)

    print("Setting up selenium")
    service = Service(ChromeDriverManager().install())
    
    print("Setting up options")
    options = webdriver.ChromeOptions()
    
    print("Starting driver")
    driver = webdriver.Chrome(service=service, options=options)

    print("Setting headers")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9'
    }

    ads = []
    for site in sites:
        print(f"Getting {site.search_url} informations")
        driver.get(site.search_url)
        
        print("Looking for cookies")
        if site.cookie_button_getter != "":
            try:
                print("Waiting for cookie button.")
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, site.cookie_button_getter))).click()
                print("Cookie button clicked.")
            except Exception as e:
                print(f"No cookie button found: {e}")
        else:
            print("No cookie button getter provided, skipping.")

        print("Parsing ads")
        ads.extend(parse(driver, site))
    
    driver.quit()
    print(ads)


if __name__ == "__main__":
    main()