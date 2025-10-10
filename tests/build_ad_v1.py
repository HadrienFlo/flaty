"""Method definitions to parse containers from websites."""

import json
import httpx
from selectolax.parser import HTMLParser
import json
from dataclasses import dataclass

@dataclass
class Site:
    name: str
    url: str
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
    keyfacts: list[str] | str
    location: str
    img: str


def load_sites():
    with open("src/sites.json", "r") as f:
        data = json.load(f)
    return [Site(**item) for item in data]


def load_page(client, url):
    response = client.get(url)
    return HTMLParser(response.text)


def parse(site, html: HTMLParser):
    url_list = html.css(site.ad_url_getter)
    price_list = html.css(site.ad_price_getter)
    keyfacts_list = html.css(site.ad_keyfacts_getter)
    location_list = html.css(site.ad_location_getter)
    img_list = html.css(site.ad_img_getter)
    return [
        Ad(
            site=site.name,
            url=url.attrs.get('href'),
            price=price.text(strip=True),
            keyfacts=keyfacts.text(strip=True),
            location=location.text(strip=True),
            img=img.attrs.get('src')
        )
        for url, price, keyfacts, location, img in zip(url_list, price_list, keyfacts_list, location_list, img_list)
    ]

def site_selector(sites, url):
    for site in sites:
        if site.url in url:
            return site
    return None

def get_ads(urls: list[str]) -> list[Ad]:
    sites = load_sites()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9'
    }
    client = httpx.Client(headers=headers)

    Ads = []

    for url in urls:
        print(f"parsing {url} informations.")
        site = site_selector(sites, url)
        html = load_page(client, url)
        ads = parse(site, html)
        print(f"{len(ads)} containers added.")
        Ads.extend(ads)
    return Ads

def ads_to_dict(ads: list[Ad]) -> dict[str, list[dict[str, str]]]:
    d = dict[str, list[dict[str, str]]]
    for ad in ads:
        if ad.site in d:
            d[ad.site].append(
                {
                    "site": ad.site,
                    "url": ad.url,
                    "price": ad.price,
                    "keyfacts": ad.keyfacts,
                    "location": ad.location,
                    "img": ad.img
                }
            )
        else:
            d[ad.site] = [
                {
                    "site": ad.site,
                    "url": ad.url,
                    "price": ad.price,
                    "keyfacts": ad.keyfacts,
                    "location": ad.location,
                    "img": ad.img
                }
            ]
    print(d)
    return d


def ads_to_list(ads: list[Ad]) -> list[dict[str, str]]:
    return [
        {
            "site": ad.site,
            "url": ad.url,
            "price": ad.price,
            "keyfacts": ad.keyfacts,
            "location": ad.location,
            "img": ad.img
        }
        for ad in ads
    ]