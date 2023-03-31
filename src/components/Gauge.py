import dash
import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs

def render_gauge(app : Dash) ->html.Div:

    @app.callback(
        #Output(component_id='fan_control', component_property='className'),
        Output(component_id='gauge_id', component_property='value'),
        Output(component_id='darktheme-daq-thermometer', component_property='value'),
        Input('interval-component', 'n_intervals')

    )
    def email_func(n):
        temperature, humidity = cs.dht11_read()
        if temperature > 20:
            cs.send_email(value, 'peacewalkerify@gmail.com')
            print("temp above 20")

        return  temperature,humidity

    @app.callback(
        Output(component_id='fan_control', component_property='className'),
        Input('interval-component', 'n_intervals'),
    )
    def process_email(n):
        cs.check_email()
        if cs.EMAIL_STATUS and cs.FAN_ON:
            #cs.turn_fan_on("ON")
            return 'fan fan_controll mt-4'
        else:
            #cs.turn_fan_on("OFF")
            return 'fan mt-4'

    return html.Div([dcc.Store(id="email_check",data={'status' : False}),daq.Gauge(
    id="gauge_id",
    color={"gradient":True,"ranges":{"green":[0,16],"yellow":[16,24],"red":[24,30]}},
    value=0,
    label="Temperature",
    size=110,
    max=30,
    min=0,
)])

