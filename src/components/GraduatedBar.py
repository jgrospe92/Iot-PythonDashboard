import dash
import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs
from . import Colors
from dash.exceptions import PreventUpdate

def render_GraduatedBar(app : dash):
    theme = {
        'dark': True,
        'detail': Colors.DARK_BLUE,  # darker
        'primary': Colors.LIGHT_BLUE,  # highlight
        'secondary': Colors.GRAY,  # base
    }
    
    @app.callback(
        Output(component_id='text_sensor_ID', component_property='children'),
        Input(component_id='LDR_bar_id', component_property='value'),prevent_initial_call=True
        )
    def update_text_sensor(value):
        return "LDR : " + str(cs.sensorValue)

    @app.callback(
        Output(component_id='LDR_bar_id', component_property='value'),
        Input('interval-light-sensor', 'n_intervals'),prevent_initial_call=True
        #Input('inteverl_for_url', 'n_intervals')
    )
    def update_light_sensor(n):
        print("intervals: " + str(cs.sensorValue))
        dataValue = cs.sensorValue
        value = round(dataValue / 100)
        return value
    graduatedbar_layout = [daq.GraduatedBar(
    color={"gradient":True,
           "ranges":{
               "#684B0D":[0,5],
               "#EFBF3E":[5,7],
               "#F9FF2F":[7,10]}},
    #showCurrentValue=True,
    id="LDR_bar_id",
    max=10),
    html.P(id="text_sensor_ID",children="LDR : 1000", className="text-warning fw-bold mt-2")]

    return html.Div(children=[
         dcc.Interval(
             id="interval-light-sensor",
             interval=1*2000, # every seconds
             n_intervals=0
         ),
        daq.DarkThemeProvider(theme=theme, children=graduatedbar_layout)], className="order-2 mt-2")
