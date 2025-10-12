import json
import logging
from dataclasses import dataclass
from rich import print

import asyncio
from pydoll.browser import Chrome

from src.utils.logger import log_function

log = logging.getLogger(__name__)

@dataclass
class Site:
    name: str
    url: str
    search_url: str
    ad_url_getter: str
    ad_price_getter: str
    ad_keyfacts_getter: str
    ad_keyfacts_children_getter: str
    ad_location_getter: str
    ad_img_getter: str


@dataclass
class Ad:
    id: int
    site: Site
    url: str
    price: str
    keyfacts: str
    keyfacts_children: str
    location: str
    img: str


def Ad_to_dict(ad: Ad) -> dict:
    return {
        "id": hash(ad.url),
        "site": ad.site.name,
        "url": ad.url,
        "price": ad.price,
        "keyfacts": ad.keyfacts,
        "keyfacts_children": ad.keyfacts_children,
        "location": ad.location,
        "img": ad.img
    }


@log_function(track_memory=True)
def load_sites(urls: dict[str, str]) -> list[Site]:
    with open("src/sites.json", "r") as f:
        data = json.load(f)
    for item in data:
        item["search_url"] = urls.get(item["name"], "")
    return [Site(**item) for item in data]


def join_children(children_list: list[str]) -> str:
    return " ".join(children_list).replace('·', '')


async def group_keyfacts(site: Site, keyfacts_list) -> list[str]:
    res = []
    for keyfacts in keyfacts_list:
            children = await keyfacts.query(site.ad_keyfacts_children_getter, find_all=True)
            children_text_list = []
            for child in children:
                child_str = await child.text
                children_text_list.append(child_str)
            res.append(join_children(children_text_list))
    return res


def check_ad_url(ad_url: str) -> bool:
    if ad_url and ad_url.startswith("http"):
        return True
    return False


def update_ad_url(ad_url: str, site: Site) -> str:
    if not check_ad_url(ad_url):
        return site.url + ad_url
    return ad_url


@log_function(track_memory=True)
async def scrap(site: Site) -> list[Ad]:
    async with Chrome() as browser:
        log.info(f"Scraping {site.name} - {site.search_url}")
        tab = await browser.start()
        await tab.go_to(site.search_url)
        url_list = await tab.query(site.ad_url_getter, find_all=True)
        price_list = await tab.query(site.ad_price_getter, find_all=True)
        keyfacts_list = await tab.query(site.ad_keyfacts_getter, find_all=True)
        keyfacts_children_list = await group_keyfacts(site, keyfacts_list)
        location_list = await tab.query(site.ad_location_getter, find_all=True)
        img_list = await tab.query(site.ad_img_getter, find_all=True)
        Ads = []
        for url, price, keyfacts, keyfacts_children, location, img in zip(url_list, price_list, keyfacts_list, keyfacts_children_list, location_list, img_list):
            ad_url = update_ad_url(url.get_attribute('href'), site)
            price = await price.text
            keyfacts = await keyfacts.text
            keyfacts_children = keyfacts_children
            location = await location.text
            img = img.get_attribute('src')
            ad = Ad(
                id = hash(ad_url),
                site = site,
                url = ad_url,
                price = price,
                keyfacts = keyfacts,
                keyfacts_children = keyfacts_children,
                location = location,
                img = img
            )
            Ads.append(ad)
        log.info(f"Got {len(Ads)} ads from {site.name}")
    return Ads