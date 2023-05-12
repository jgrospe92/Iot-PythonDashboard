import dash_daq as daq
import dash
import time
from dash import Dash, html, Input, Output, State
from dash.exceptions import PreventUpdate
import src.Controller.ControllerSystem as cs
from src.Controller.Scanner import *
from . import Colors

def render_toggleSwitch(app: Dash, on, off):
    theme = {
        'dark': True,
        'detail': Colors.DARK_BLUE,  # darker
        'primary': Colors.LIGHT_BLUE,  # highlight
        'secondary': Colors.GRAY,  # base
    }
    @app.callback(
        [Output(component_id='ble_control', component_property='src'),
         Output(component_id='num_ble_devices', component_property='children'),
         Output(component_id='blu_status', component_property='children')],
        [Input(component_id='toggleSwitchId', component_property='value')],
        [State(component_id='rssi_input', component_property='value')],
        prevent_initial_call=True
    )
    def update(switch, rssi):
        print(switch)
        print(rssi)
        if switch:
            if rssi is None:
                count = [device for device in run_scanner(2) if abs(int(device[2])) > 0]
                cs.BT_counter = len(count)
                return on , cs.BT_counter, 'done'
            else:
                count = [device for device in run_scanner(2) if abs(int(device[2])) > rssi]
                cs.BT_counter = len(count)
                return on , cs.BT_counter, 'done'
        else:
            end_inquiry()
            return off, 0, ''

    layout = daq.ToggleSwitch(
        id="toggleSwitchId",
        vertical=True,
        value=False,
        size=50,
        labelPosition='bottom',
    )
    return html.Div(children=[daq.DarkThemeProvider(theme=theme, children=layout)])
