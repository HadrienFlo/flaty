import logging
import dash
from dash import callback, Input, State, Output
import dash_mantine_components as dmc
from dash.html import Div

log = logging.getLogger(__name__)


@callback(Output("chip-container", "children"), Input("chip-state", "checked"))
def checkbox(checked):
    return f"The chip is selected: {checked}"