import dash
import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs
from . import Colors


def render_GraduatedBar(app : dash):

    theme = {
        'dark': True,
        'detail': Colors.DARK_BLUE,  # darker
        'primary': Colors.LIGHT_BLUE,  # highlight
        'secondary': Colors.GRAY,  # base
    }

    graduatedbar_layout = daq.GraduatedBar(
    color={"gradient":True,
           "ranges":{
               "#684B0D":[0,5],
               "#EFBF3E":[5,7],
               "#F9FF2F":[7,10]}},
    showCurrentValue=True,
    value=10,
    label='light intensity',
    labelPosition='bottom',
    max=10)

    return html.Div(children=[daq.DarkThemeProvider(theme=theme, children=graduatedbar_layout)], className="order-2 mt-2")
