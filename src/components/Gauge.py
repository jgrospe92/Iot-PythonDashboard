import dash_daq as daq
from dash import Dash, html


def render_gauge(app : Dash) ->html.Div:
    return html.Div([daq.Gauge(
    color={"gradient":True,"ranges":{"green":[0,16],"yellow":[16,24],"red":[24,30]}},
    value=2,
    size=110,
    max=30,
    min=0,
)])

