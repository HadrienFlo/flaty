"""
This module defines the search input components and search logic for a Dash application using Dash Mantine Components (dmc).
It provides UI elements for users to input search criteria for real estate ads and handles the asynchronous scraping and display of results.
Functions:
-----------
- build_ad_card(ad: Ad):
    Constructs a dmc.Card component displaying information about a real estate ad.
- store_search(n_clicks, city, max_rent, min_area, min_rooms):
    Dash callback. Asynchronously scrapes real estate ads from multiple sources based on user input.
    Returns the search URLs, list of ads, and accordion state for UI updates.
- update_search(urls, ads, accordion_state):
    Dash callback. Updates the UI with the search URLs and the list of ads as dmc components.
Variables:
-----------
- app: Dash app instance.
- server: Flask server instance from the Dash app.
- page_color_theme: Color theme for the page, derived from dmc default theme.
- style: Dictionary for component styling.
- layout: dmc.Group containing the search input fields and search button.
Dependencies:
-------------
- dash, dash_mantine_components, asyncio, logging, json, dataclasses, rich
- src.utils.logger, src.build_url, src.manager
Note:
-----
- The module expects certain utility functions and classes (e.g., Ad, scrap, Ad_to_dict, load_sites) to be defined in the src package.
- The callbacks use Dash's async capabilities for concurrent scraping.
"""

import dash
from dash import callback, Input, State, Output, get_app
dash._dash_renderer._set_react_version("18.2.0")

import dash_mantine_components as dmc

import logging
from rich import print

import asyncio

from components.SearchInputs.build_ad_card import build_ad_card
from src.url_factory import pap_url, seloger_url, bienici_url
from src.manager import scrap, Ad_to_dict, load_sites

log = logging.getLogger(__name__)

app = get_app()
server = app.server

page_color_theme = dmc.DEFAULT_THEME["colors"]["blue"][6]
style = {
    "justifyItems": "center",
}

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

    log.info(f"Found {len(ads_list)} ads")

    # list[Ad] -> list[dict]
    ad_list = []
    for ads in ads_list:
        ad_list.extend([Ad_to_dict(ad) for ad in ads])

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