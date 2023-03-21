import dash_daq as daq
from dash import Dash, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import src.Controller.ControllerSystem as cs
from . import Colors

theme = {
    'dark': True,
    'detail': Colors.DARK_BLUE, # darker
    'primary': Colors.LIGHT_BLUE, # highlight
    'secondary': Colors.GRAY, # base
}

def render_thermo(app: Dash):
    @app.callback(
        Output("fan_control", "style"),
        Input('darktheme-daq-thermometer', 'value'))
    def thermo_callback(value):
        print("thermo is " + str(value))


#here must be changed for the value of cs.fan_spin
    thermo_layout = html.Div([daq.Thermometer(
        min=0,
        max=30,
        #here should be the temperature value that's used in Controller system
        value=dht.temperature,
        showCurrentValue=True,
        height=110,
        width=8,
        units="C",
        id='darktheme-daq-thermometer',
        className='dark-theme-control')])

    return html.Div(children=[daq.DarkThemeProvider(theme=theme, children=thermo_layout)])
