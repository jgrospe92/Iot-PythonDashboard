import dash
import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs
from src.Helper import SqLiteDbHelper as dbHelper
def render_gauge(app : Dash) ->html.Div:

    @app.callback(
        #Output(component_id='fan_control', component_property='className'),
        Output(component_id='gauge_id', component_property='value'),
        Output(component_id='darktheme-daq-thermometer', component_property='value'),
        Input('interval-component', 'n_intervals'),prevent_initial_call=True

    )
    def email_func(n):
        #temperature, humidity = cs.dht11_read()
        if temperature > dbHelper.current_user_data[2]:
            pass
            #cs.send_email(temperature, 'peacewalkerify@gmail.com')
            

        #return  temperature,humidity
        return 0,0
        

    @app.callback(
        Output(component_id='fan_control', component_property='className'),
        Input('interval-component', 'n_intervals'),prevent_initial_call=True
    )
    def process_email(n):
        #cs.check_email()
        if cs.EMAIL_STATUS and cs.FAN_ON:
            cs.turn_fan_on("ON")
            return 'fan fan_controll mt-4'
        else:
            cs.turn_fan_on("OFF")
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

