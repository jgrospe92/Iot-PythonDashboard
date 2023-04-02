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

    @app.callback(
        Output(component_id='LDR_bar_id', component_property='value'),
        Input('interval-light-sensor', 'n_intervals')
    )
    def update_light_sensor(n):
        value = round(cs.sensorValue/ 100)
        return value

    graduatedbar_layout = daq.GraduatedBar(
    color={"gradient":True,
           "ranges":{
               "#684B0D":[0,5],
               "#EFBF3E":[5,7],
               "#F9FF2F":[7,10]}},
    showCurrentValue=True,
    value=0,
    label='light intensity',
    labelPosition='bottom',
    id="LDR_bar_id",
    max=10)

    return html.Div(children=[
        dcc.Interval(
            id="interval-light-sensor",
            interval=1 * 2000, # every two seconds
            n_intervals=0
        ),
        daq.DarkThemeProvider(theme=theme, children=graduatedbar_layout)], className="order-2 mt-2")
