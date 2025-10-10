"""Some method definitions."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_pap_geo_code(query: str) -> list[dict[str, str]]:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.pap.fr/json/ac-geo?q=" + query)
    content = driver.page_source
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)
    driver.quit()
    return parsed_json