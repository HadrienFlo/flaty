import dash
from dash import callback, Input, State, Output, get_app
dash._dash_renderer._set_react_version("18.2.0")

import dash_mantine_components as dmc

import json
from dataclasses import dataclass
from rich import print

import asyncio
from pydoll.browser import Chrome

from src.build_url import pap_url, seloger_url, bienici_url
# from src.manager import Ad, scrap


app = get_app()
server = app.server


page_color_theme = dmc.DEFAULT_THEME["colors"]["blue"][6]
style = {
    "justifyItems": "center",
}

@dataclass
class Site:
    name: str
    url: str
    search_url: str
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


def Ad_to_dict(ad: Ad) -> dict:
    return {
        "site": ad.site.name,
        "url": ad.url,
        "price": ad.price,
        "keyfacts": ad.keyfacts,
        "location": ad.location,
        "img": ad.img
    }


def load_sites(urls: dict[str, str]) -> list[Site]:
    with open("src/sites.json", "r") as f:
        data = json.load(f)
    for item in data:
        item["search_url"] = urls.get(item["name"], "")
    return [Site(**item) for item in data]


async def parse(driver, site: Site):
    await driver.go_to(site.search_url)
    url_list = await driver.query(site.ad_url_getter, find_all=True)
    price_list = await driver.query(site.ad_price_getter, find_all=True)
    keyfacts_list = await driver.query(site.ad_keyfacts_getter, find_all=True)
    location_list = await driver.query(site.ad_location_getter, find_all=True)
    img_list = await driver.query(site.ad_img_getter, find_all=True)
    Ads = [
        Ad(
            site=site,
            url=url.get_attribute('href'),
            price=price.value,
            keyfacts=keyfacts.value,
            location=location.value,
            img=img.get_attribute('src')
        )
        for url, price, keyfacts, location, img in zip(url_list, price_list, keyfacts_list, location_list, img_list)
    ]
    return Ads


async def scrap(site: Site) -> list[Ad]:
    async with Chrome() as browser:
        print(f"Scraping {site.name} - {site.search_url}")
        tab = await browser.start()
        # if not site or (isinstance(site.search_url, str) and site.search_url.strip() == ""):
        #     return []
        await tab.go_to(site.search_url)
        url_list = await tab.query(site.ad_url_getter, find_all=True)
        price_list = await tab.query(site.ad_price_getter, find_all=True)
        keyfacts_list = await tab.query(site.ad_keyfacts_getter, find_all=True)
        location_list = await tab.query(site.ad_location_getter, find_all=True)
        img_list = await tab.query(site.ad_img_getter, find_all=True)
        Ads = [
            Ad(
                site=site,
                url=url.get_attribute('href'),
                price=price.text,
                keyfacts=keyfacts.text,
                location=location.text,
                img=img.get_attribute('src')
            )
            for url, price, keyfacts, location, img in zip(url_list, price_list, keyfacts_list, location_list, img_list)
        ]
    return Ads


def build_ad_card(ad: Ad):
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src=ad.get("img", "https://via.placeholder.com/300x160.png?text=No+Image"),
                    h=160,
                    alt="Norway",
                )
            ),
            dmc.Group(
                [
                    dmc.Text(ad.get("price", ""), fw=500),
                    dmc.Badge(ad.get("site", ""), color="pink"),
                ],
                justify="space-between",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "%s - %s" % (ad.get("keyfacts", "No keyfacts found"), ad.get("location", "No location found")),
                size="sm",
                c="dimmed",
            ),
            dmc.Anchor(
                dmc.Button(
                    "Open Ad",
                    color="blue",
                    fullWidth=True,
                    mt="md",
                    radius="md",
                ),
                href=ad.get("url", "#"), target="_blank"
            )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w=350,
    )


@callback(
    Output("store_search_urls", "data"),
    Output("store_search_ads", "data"),
    Output("store_search_accordion_state", "data"),
    Input("search_button", "n_clicks"),
    State("city_intput", "value"),
    State("max_rent_input", "value"),
    State("min_area_input", "value"),
    State("min_rooms_input", "value"),
    running=[
        (Output("search_button", "loading"), True, False),
        (Output("search_loading_overlay", "visible"), True, False),
    ]
)
async def store_search(n_clicks, city, max_rent, min_area, min_rooms):
    if not n_clicks or not city:
        raise dash.exceptions.PreventUpdate

    seloger = seloger_url(city, max_rent, min_area, min_rooms)
    pap = pap_url(city, max_rent, min_area, min_rooms)
    bienici = bienici_url(city, max_rent, min_area, min_rooms)

    urls = {
        "SeLoger": seloger,
        "PAP": pap,
        "Bien'ici": bienici
    }
    sites = load_sites(urls)

    coros = [scrap(site) for site in sites[:2]]
    ads_list = await asyncio.gather(*coros)
    print(ads_list)
    ad_list = []
    for ads in ads_list:
        ad_list.extend([Ad_to_dict(ad) for ad in ads])

    for ad in ad_list:
        print(ad)

    accordion_active_value = ["search_output_urls"]

    return urls, ad_list, accordion_active_value


@callback(
    Output("search_output_urls", "children"),
    Output("search_output_ads", "children"),
    Output("search_output_accordion", "value"),
    Input("store_search_urls", "data"),
    State("store_search_ads", "data"),
    State("store_search_accordion_state", "data"),
    running=[
        (Output("search_button", "loading"), True, False),
        (Output("search_loading_overlay", "visible"), True, False),
    ]
)
def update_search(urls, ads, accordion_state):
    if not urls and not ads:
        raise dash.exceptions.PreventUpdate
    
    print(f"From update_search:\nurls: {len(urls)}\nads: {len(ads)}")

    output_urls = dmc.Group([
        dmc.Anchor(dmc.Button(u_name, color="blue", mt="md", radius="md", variant="outline"), href=u_url, target="_blank")
        for u_name, u_url in urls.items()
    ])

    output_ads = dmc.Grid(
        children=[
            dmc.GridCol(
                dmc.Box(
                    build_ad_card(ad), 
                    style=style
                ), 
                span={"base": 12, "md": 6, "lg":3}
            )
            for ad in ads
        ]
    )
    return output_urls, output_ads, accordion_state


layout = dmc.Group([
    dmc.TextInput(label="City", id="city_intput", placeholder="e.g., Paris", style={"width": 300}, size="md", persistence=True),
    dmc.NumberInput(label="Max Rent (€)", id="max_rent_input", placeholder="e.g., 1200", style={"width": 150}, size="md", persistence=True),
    dmc.NumberInput(label="Min Area (m²)", id="min_area_input", placeholder="e.g., 30", style={"width": 150}, size="md", persistence=True),
    dmc.NumberInput(label="Min Rooms", id="min_rooms_input", placeholder="e.g., 2", style={"width": 150}, size="md", persistence=True),
    dmc.Button("Search", id="search_button", n_clicks=0, loaderProps={"type": "dots"}, style={"margin-top": 24}, color=page_color_theme, variant="light"),
])