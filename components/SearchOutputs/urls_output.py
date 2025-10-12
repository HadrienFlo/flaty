import logging
import dash
from dash import callback, Input, Output
from dash.html import Div
import dash_mantine_components as dmc
from components.SearchOutputs.build_url_button import build_url_button

log = logging.getLogger(__name__)

@callback(
    Output("search_output_urls", "children"),
    Input("store_search_urls", "data"),
    running=[
        (Output("search_button", "loading"), True, False),
        (Output("search_loading_overlay", "visible"), True, False),
    ]
)
def update_urls(urls):
    if not urls:
        raise dash.exceptions.PreventUpdate
    
    log.info(f"Updating urls output with {urls}")
    output_urls = dmc.Group([
        build_url_button(u_name, u_url)
        for u_name, u_url in urls.items()
    ])

    return output_urls


layout = Div(id="search_output_urls")