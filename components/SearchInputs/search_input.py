"""
This module provides the search input UI and asynchronous search logic for a Dash application focused on real estate ads.
It leverages Dash Mantine Components for the UI and integrates with custom scraping utilities to fetch ads from multiple sources.
Main Components and Functions:
------------------------------
- `layout`: A Dash Mantine Group containing input fields for city, max rent, min area, min rooms, and a search button.
- `store_search`: An async Dash callback that triggers on search button click, constructs search URLs, scrapes ads concurrently, and stores results for UI updates.
Key Variables:
--------------
- `app`: The Dash app instance.
- `server`: The Flask server instance from the Dash app.
- `page_color_theme`: The primary color theme for the page.
- `style`: Styling dictionary for component alignment.
- dash, dash_mantine_components, asyncio, logging, rich
- src.url_factory (for URL construction)
- src.manager (for scraping and ad serialization)
Notes:
------
- The module expects utility functions and classes (e.g., `scrap`, `Ad_to_dict`, `load_sites`) to be defined in the `src` package.
- The callback uses Dash's async capabilities for concurrent scraping.
- The UI is designed for real estate ad search and display.
"""
import logging
import asyncio

import dash
from dash import callback, Input, State, Output, get_app
dash._dash_renderer._set_react_version("18.2.0")
import dash_mantine_components as dmc

from components.SearchOutputs.build_url_button import build_url_button
from components.SearchOutputs.build_ad_card import build_ad_card

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


layout = dmc.Group([
    dmc.TextInput(label="City", id="city_intput", placeholder="e.g., Paris", style={"width": 300}, size="md", persistence=True),
    dmc.NumberInput(label="Max Rent (€)", id="max_rent_input", placeholder="e.g., 1200", style={"width": 150}, size="md", persistence=True),
    dmc.NumberInput(label="Min Area (m²)", id="min_area_input", placeholder="e.g., 30", style={"width": 150}, size="md", persistence=True),
    dmc.NumberInput(label="Min Rooms", id="min_rooms_input", placeholder="e.g., 2", style={"width": 150}, size="md", persistence=True),
    dmc.Button("Search", id="search_button", n_clicks=0, loaderProps={"type": "dots"}, style={"margin-top": 24}, color=page_color_theme, variant="light"),
])