import dash
from dash import get_app
dash._dash_renderer._set_react_version("18.2.0")

import dash_mantine_components as dmc


app = get_app()

dash.register_page(__name__, path="/views", title="Views")


layout = dmc.Group([dmc.Text("Text3", id='input2'), dmc.Text("Text4", id='output2')])
