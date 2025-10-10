
import time
from dash import html, Input, Output, Dash
import asyncio

app = Dash()
server = app.server

def get_sync_data(iteration):
    time.sleep(1) 
    return f"Result ({iteration}) from synchronous API call"

async def get_async_data(iteration):
    await asyncio.sleep(1)
    return f"Result ({iteration}) from asynchronous API call"

app.layout = html.Div([
    html.H2("Synchronous vs. Asynchronous Functions in Dash"),
    html.Button("Run Sync Tasks", id="sync-btn", style={'margin-right': '10px'}),
    html.Button("Run Async Tasks", id="async-btn"),
    html.Hr(),
    html.Div(id="sync-output", style={'color': 'red', 'font-weight': 'bold'}),
    html.Div(id="async-output", style={'color': 'green', 'font-weight': 'bold'}),
])

@app.callback(
    Output("sync-output", "children"),
    Input("sync-btn", "n_clicks"),
    prevent_initial_call=True,
)
def sync_callback_example(n_clicks):
    if n_clicks:
        results = [get_sync_data(i) for i in range(5)]
        return html.Div([html.Div(result) for result in results])
    return ""

@app.callback(
    Output("async-output", "children"),
    Input("async-btn", "n_clicks"),
    prevent_initial_call=True,
)
async def async_callback_example(n_clicks):
    if n_clicks:
        coros = [get_async_data(i) for i in range(5)]
        results = await asyncio.gather(*coros)
        return html.Div([html.Div(result) for result in results])
    return ""

if __name__ == "__main__":
    app.run(debug=True, port=8051)
