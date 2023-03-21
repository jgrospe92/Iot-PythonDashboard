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
        Output(component_id='fan_control', component_property='className'),
        Input(component_id='darktheme-daq-thermometer', component_property='value')
    )
    def email_func(value):
        if value is None:
            raise PreventUpdate
        else:
            if value > 24:
                cs.send_email(value, 'peacewalkerify@gmail.com')
                return 'fan fan_controll mt-4'
            else :
                return 'fan mt-4'

    thermo_layout = html.Div([daq.Thermometer(
        min=0,
        max=30,
        value=26,
        showCurrentValue=True,
        height=110,
        width=8,
        units="C",
        id='darktheme-daq-thermometer',
        className='dark-theme-control')])

    return html.Div(children=[daq.DarkThemeProvider(theme=theme, children=thermo_layout)])
