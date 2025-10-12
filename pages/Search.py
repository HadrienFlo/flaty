import dash
from dash import get_app, dcc
dash._dash_renderer._set_react_version("18.2.0")

import dash_mantine_components as dmc

from components.SearchInputs.search_input import layout as search_inputs_layout
from components.SearchOutputs.ads_output import layout as search_outputs_ads_layout
from components.SearchOutputs.urls_output import layout as search_outputs_urls_layout

app = get_app()

dash.register_page(__name__, path="/", title="Search")

page_color_theme = dmc.DEFAULT_THEME["colors"]["blue"][6]

# (city, max_rent, furnished, minimum_area, minimum_rooms)


layout = dmc.Stack([
    # search stores
    dcc.Store(id='store_search_urls', storage_type="session"),
    dcc.Store(id='store_search_ads', storage_type="session"),
    dcc.Store(id='store_search_accordion_state', storage_type="session"),
    # search inputs
    search_inputs_layout,
    #search outputs
    dmc.Divider(color=page_color_theme),
    dmc.Group([
        dmc.LoadingOverlay(
            visible=False,
            id="search_loading_overlay",
            overlayProps={"radius": "sm", "blur": 2},
            zIndex=10,
        ),
        dmc.Accordion(
            id="search_output_accordion",
            multiple=True,
            persistence=True,
            persistence_type="session",
            children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            dmc.Group([
                                dmc.Avatar(src="https://img.icons8.com/?size=100&id=zxPKFbyNX7i6&format=png&color=4dabf7", size=24),
                                dmc.Text("Generated URLs", style={"fontWeight": "bold"}),
                            ])
                        ),
                        dmc.AccordionPanel(
                            search_outputs_urls_layout,
                        ),
                    ],
                    value="search_output_urls",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            dmc.Group([
                                dmc.Avatar(src="https://img.icons8.com/?size=100&id=RYcCGyq4E6Bv&format=png&color=4dabf7", size=24),
                                dmc.Text("Ads overview", style={"fontWeight": "bold"}),
                            ])
                        ),
                        dmc.AccordionPanel(
                            search_outputs_ads_layout,
                        ),
                    ],
                    value="search_output_ads",
                ),
            ],
            chevronPosition="left",
	    variant="separated",
            radius="md",
            style={"width": "100%"},
        ),
    ]),
], gap="lg", style={"padding": 20})