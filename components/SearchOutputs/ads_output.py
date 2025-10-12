import logging
import dash
from dash import callback, Input, Output
from dash.html import Div
import dash_mantine_components as dmc
from components.SearchOutputs.build_ad_card import build_ad_card

log = logging.getLogger(__name__)

@callback(
    Output("search_output_ads", "children"),
    Input("store_search_ads", "data"),
    running=[
        (Output("search_button", "loading"), True, False),
        (Output("search_loading_overlay", "visible"), True, False),
    ]
)
def update_ads(ads):
    if not ads:
        raise dash.exceptions.PreventUpdate

    log.info(f"Updating ads output with {len(ads)} ads")
    output_ads = dmc.Grid(
        children=[
            dmc.GridCol(
                dmc.Box(
                    build_ad_card(ad), 
                    style={"justifyItems": "center"}
                ), 
                span={"base": 12, "md": 6, "lg":3}
            )
            for ad in ads
        ]
    )

    return output_ads


layout = Div(id="search_output_ads")