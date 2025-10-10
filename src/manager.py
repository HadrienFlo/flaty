import json
from dataclasses import dataclass

import asyncio
from pydoll.browser import Chrome


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
            price=price.text.strip(),
            keyfacts=keyfacts.text.strip(),
            location=location.text.strip(),
            img=img.get_attribute('src')
        )
        for url, price, keyfacts, location, img in zip(url_list, price_list, keyfacts_list, location_list, img_list)
    ]
    return Ads


async def scrap(urls: dict[str, str]) -> dict[str, list[Ad]]:
    async with Chrome() as browser:
        sites = load_sites(urls)
        ads = {}
        tab = await browser.start()
        for site in sites:
            if not site.search_url:
                continue
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
            ads[site.name] = Ads
    return ads
