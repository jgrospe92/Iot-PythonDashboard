import dash_daq as daq
from dash import Dash, html, Input, Output
from dash.exceptions import PreventUpdate
from . import Colors

def render_toggleSwitch(app: Dash, on, off):
    theme = {
        'dark': True,
        'detail': Colors.DARK_BLUE,  # darker
        'primary': Colors.LIGHT_BLUE,  # highlight
        'secondary': Colors.GRAY,  # base
    }
    @app.callback(
        Output(component_id='ble_control', component_property='src'),
        Input(component_id='toggleSwitchId', component_property='value'),prevent_initial_call=True
    )
    def update(value):
        if value is None:
            raise PreventUpdate
        return on if value else off

    layout = daq.ToggleSwitch(
        id="toggleSwitchId",
        vertical=True,
        value=False,
        size=50,
        labelPosition='bottom',
    )
    return html.Div(children=[daq.DarkThemeProvider(theme=theme, children=layout)])
