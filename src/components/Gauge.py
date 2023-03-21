import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs

def render_gauge(app : Dash) ->html.Div:
    @app.callback(
        Output(component_id='fan_control', component_property='className'),
        Input(component_id='gauge_id', component_property='value')
    )
    def email_func(value):
        if value is None:
            raise PreventUpdate
        else:
            if value > 24:
                # cs.send_email(value, 'peacewalkerify@gmail.com')
                print(value)
                return 'fan fan_controll mt-4'
            else:
                return 'fan mt-4'

    return html.Div([daq.Gauge(
    id="gauge_id",
    color={"gradient":True,"ranges":{"green":[0,16],"yellow":[16,24],"red":[24,30]}},
    value=25,
    label="Temperature",
    size=110,
    max=30,
    min=0,
)])

