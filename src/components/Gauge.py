import dash_daq as daq
from dash import Dash, html, Input, Output, dcc
import src.Controller.ControllerSystem as cs

def render_gauge(app : Dash) ->html.Div:
    @app.callback(
        #Output(component_id='fan_control', component_property='className'),
        Output('email_check','data'),
        Input(component_id='gauge_id', component_property='value'),
        Input('email_check', 'data')

    )
    def email_func(value, data):
        print("data status ", end="")
        print(data['status'])
        if value > 24 and not data['status']:
            # cs.send_email(value, 'peacewalkerify@gmail.com')
            print(value)
            #return 'fan fan_controll mt-4'
            return {'status' : True}
        else:
            #return 'fan mt-4'
            return {'status' : False}

    @app.callback(
        Output('fake', 'children'),
        Input('email_check', 'data')
    )
    def test(data):
        print('data is ', end="")
        print(data['status'])


    return html.Div([dcc.Store(id="email_check",data={'status' : False}),daq.Gauge(
    id="gauge_id",
    color={"gradient":True,"ranges":{"green":[0,16],"yellow":[16,24],"red":[24,30]}},
    #cs.fan_spin values must be here
    value=dht.temperature,
    label="Temperature",
    size=110,
    max=30,
    min=0,
)])

