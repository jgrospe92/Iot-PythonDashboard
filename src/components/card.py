# This is a sample of a component class
import time
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import html, Dash, dcc
from dash.dependencies import Input, Output
import src.Controller.ControllerSystem as cs
import dash_daq as daq
from . import Colors
from . import Gauge
from . import Thermometer
from . import GraduatedBar


def render_card(app: Dash) -> html.Div:
    email_sent = "https://cdn-icons-png.flaticon.com/512/2593/2593557.png"
    email_default = "https://cdn-icons-png.flaticon.com/512/896/896673.png"
    light_off_icon = "https://cdn-icons-png.flaticon.com/512/3626/3626525.png"
    light_on_icon = "https://cdn-icons-png.flaticon.com/512/3625/3625060.png"

    # Add the callbacks
    # email icon callbacks
    @app.callback(
        Output(component_id='email_statusID', component_property="src"),
        Input('LDR_bar_id', 'value'),
    )
    def update_email_icon(value):
        if value is None:
            raise PreventUpdate
        else:
            cs.send_email_light_sensor("peacewalkerify@gmail.com")
            if cs.EMAIL_SENSOR_STATUS:
                return email_sent
            else:
                return email_default

    # Callbacks for the light switch
    @app.callback(
        # Output(component_id='btn-activate', component_property='children'),
        # Input(component_id='btn-activate', component_property='n_clicks'),
        Output(component_id='lightbulb', component_property="src"),
        Input('LDR_bar_id', 'value'),
    )
    def update_light_icon(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        else:
            return light_on_icon if cs.light_switch_sensor() else light_off_icon

    profile = html.Div(className="profile_styling",
                       children=[dbc.Card(className="h-100",children=[dbc.CardHeader("User Profile"),
                                           dbc.CardImg(src="https://randomuser.me/api/portraits/men/90.jpg",
                                                       top=True,
                                                       style={"width": "10rem",
                                                              "border-radius": "50%",
                                                              "align-self": "center",
                                                              "justify-self": "center",
                                                              "margin-top": "50px"}),
                                           dbc.CardBody([
                                               html.H5("User Profile", className="card-title"),
                                               html.P(
                                                   "Name:",
                                                   className="card-text",
                                               ),
    
                                               html.P(
                                                   "Temperature Threshold"
                                               ),
                                               html.P(
                                                   "Humidity Threshold"
                                               ),
                                               html.P(
                                                   "Light Intensity Threshold"
                                               ),
                                             
                                           ])])])

    card_1 = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("LED CONTROL", className="card-title", id="fake"),
                    html.Div([
                        html.Img(id="email_statusID", className="email_icon",
                                 src=email_default),
                        html.Img(id="lightbulb", className="light order-1",
                                 src=light_off_icon)],
                        className="d-flex justify-content-evenly"),
                    html.Div([
                        GraduatedBar.render_GraduatedBar(app)
                        ,
                    ], className="d-flex flex-column justify-content-center align-items-center"),
                ],
            )
        )

    card_2 = dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("TEMP Control", className="card-title"),
                        # dcc.Interval(
                        #     id="interval-component",
                        #     interval=1 * 2000, # every two seconds
                        #     n_intervals=0
                        # ),
                        # html.P(className="text-warning",children="Turn the fan > 24"),
                        html.Div([
                            Gauge.render_gauge(app), Thermometer.render_thermo(app),
                            html.Img(id="fan_control", className="fan mt-4",
                                     src="https://cdn-icons-png.flaticon.com/512/545/545932.png")],
                            className="d-flex flex-row justify-content-evenly")
                    ],
                )
            )
    # Blue-tooth controller
    card_3 = dbc.Card(
                className="blue_tooth_styling",
                children=
                dbc.CardBody(
                    [
                        html.H5("Blue-Tooth Connection", className="card-title"),
                        # dcc.Interval(
                        #     id="interval-component",
                        #     interval=1 * 2000, # every two seconds
                        #     n_intervals=0
                        # ),
                        # html.P(className="text-warning",children="Turn the fan > 24"),
                        html.Div([
                            html.Img(id="fan_control2", className="fan mt-4",
                                     src="https://cdn-icons-png.flaticon.com/512/660/660354.png")
                        ],
                            className="d-flex flex-row justify-content-evenly")
                    ],
                )
            )

    cardlayout = html.Div(style={'height':'600px'},children=
        [
            dbc.Row([
                dbc.Col(profile, width=4),
                dbc.Col(html.Div([
                    dbc.Row(
                        [
                            dbc.Col(card_1),
                            dbc.Col(card_2),
                        ]
                    ),
                    dbc.Row(className="mt-2",
                            children=dbc.Col(card_3)
                    )
                ]))
            ]),
        ]
    )
    return cardlayout
