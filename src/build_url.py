from src.constants import SELOGER_PARIS_CODES
from src.utils import get_pap_geo_code


def leboncoin_url(city, max_rent, furnished, minimum_area, minimum_rooms):
    base = "https://www.leboncoin.fr/recherche?category=10"
    params = []
    # Ville (remplace espaces par _ et ajoute _75000 si Paris)
    city_param = city.replace(" ", "_")
    if "paris" in city.lower():
        city_param = "Paris_75000"
    params.append(f"locations={city_param}")
    params.append("real_estate_type=1")  # 1 = location
    if furnished.lower() in ["oui", "yes"]:
        params.append("furnished=1")
    if max_rent:
        params.append(f"price=0-{max_rent}")
    if minimum_rooms:
        params.append(f"rooms={minimum_rooms}-")
    if minimum_area:
        params.append(f"square={minimum_area}-")
    return base + "&" + "&".join(params)


def pap_url(city, max_rent, minimum_area, minimum_rooms):
    # Ex: https://www.pap.fr/annonce/locations-paris-75-g439-jusqu-a-1200-euros-a-partir-de-30-m2-2-pieces
    city_list = city.split(", ")
    url_left = ""
    for i, c in enumerate(city_list):
        c = c.lower().replace(" ", "-")
        c_geo = get_pap_geo_code(c)
        if not c_geo:
            continue
        c_geo = c_geo[0]
        c_code, c_label = c_geo['id'], c_geo['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')
        if i == 0:
            url_left += f"{c_label}-g{c_code}"
        else:
            url_left += f"g{c_code}"
    url = f"https://www.pap.fr/annonce/locations-{url_left}"
    if minimum_rooms:
        if minimum_rooms == "1":
            url += f"-studo"
        else:
            url += f"-a-partir-du-{minimum_rooms}-pieces"
    if max_rent:
        url += f"-jusqu-a-{max_rent}-euros"
    if minimum_area:
        url += f"-a-partir-de-{minimum_area}-m2"
    return url

def bienici_url(city, max_rent, minimum_area, minimum_rooms):
    # Ex: https://www.bienici.com/recherche/location/paris-75/appartement?prixMax=1200&surfaceMin=30&nbPiecesMin=2
    city_slug = city.lower().replace(" ", "-")
    url = f"https://www.bienici.com/recherche/location/{city_slug}-75/appartement?"
    params = []
    if max_rent:
        params.append(f"prixMax={max_rent}")
    if minimum_area:
        params.append(f"surfaceMin={minimum_area}")
    if minimum_rooms:
        params.append(f"nbPiecesMin={minimum_rooms}")
    return url + "&".join(params)

def seloger_url(city, max_rent, minimum_area, minimum_rooms):
    # https://www.seloger.com/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations=AD08FR31096&numberOfBedroomsMin=1&numberOfRoomsMin=2&priceMax=1200&spaceMin=30
    codes = []
    if city.lower().startswith("paris "):
        city = city.lower().replace("paris ", "").split(",")
        for arr in city:
            code = SELOGER_PARIS_CODES.get(arr)
            if code:
                codes.append(code)
    elif city.lower() == "paris":
        codes.append(SELOGER_PARIS_CODES["paris"])
    else:
        code = SELOGER_PARIS_CODES.get(city.lower())
        if code:
            codes.append(code)
    locations = ",".join(codes)
    url = f"https://www.seloger.com/classified-search?distributionTypes=Rent&estateTypes=Apartment&locations={locations}"
    if max_rent:
        url += f"&priceMax={max_rent}"
    if minimum_area:
        url += f"&spaceMin={minimum_area}"
    if minimum_rooms:
        url += f"&numberOfRoomsMin={minimum_rooms}"
    return url