# This is a sample of a component class
import time
import dash_bootstrap_components as dbc
from dash import html, Dash, dcc
from dash.dependencies import Input, Output
import src.Controller.ControllerSystem as cs
import dash_daq as daq
from . import Colors
from . import Gauge
from . import Thermometer
from . import GraduatedBar
def render_card(app: Dash) -> html.Div:
    # Add the callbacks
    # Callbacks for the button switch
    @app.callback(
        # Output(component_id='btn-activate', component_property='children'),
        # Input(component_id='btn-activate', component_property='n_clicks'),
        Output(component_id='lightbulb', component_property="src"),
        Input('our-power-button-1', 'on'),
    )
    def update_button(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        else:
            # Tenary operator return OFF if condiion is == 0 else ON
            return "https://cdn-icons-png.flaticon.com/512/3626/3626525.png" if cs.light_controller() == 0 else "https://cdn-icons-png.flaticon.com/512/3625/3625060.png"

    profile = html.Div(className="container h-100",
                       children=[dbc.Card([dbc.CardHeader("User Profile"),
                                           dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/560/560277.png",
                                                       top=True,
                                                       style={"width": "10rem",
                                                              "border-radius": "50%",
                                                              "align-self": "center",
                                                              "justify-self": "center"}),
                                           dbc.CardBody([
                                               html.H5("User Profile", className="card-title"),
                                               html.P(
                                                   "Username",
                                                   className="card-text",
                                               ),
                                               html.P(
                                                   "Favorites"
                                               ),
                                               html.P(
                                                   "Temperature"
                                               ),
                                               html.P(
                                                   "Humidity"
                                               ),
                                               html.P(
                                                   "Light Intensity"
                                               ),
                                               dbc.Button(
                                                   "Log out", color="success", className="mt-auto"
                                               ),
                                           ])])])
    cards = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("LED CONTROL", className="card-title", id="fake"),
                        html.P(
                            "Turn the switch on or off.",
                            className="card-text text-warning",
                        ),
                        html.Div([
                            # daq.PowerButton(
                            #     id='our-power-button-1',
                            #     on=True,
                            #     size=100,
                            #     color=Colors.GREEN,
                            #     className="order-2"
                            # ),
                            # html.Div(id='power-button-result-1')
                            GraduatedBar.render_GraduatedBar(app)
                            ,
                            html.Div(html.Img(id="lightbulb",className="light order-1",src="https://cdn-icons-png.flaticon.com/512/3625/3625060.png"),className="light-container")
                        ],className="d-flex flex-column justify-content-center align-items-center"),
                    ],
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("TEMP Control", className="card-title"),
                        # dcc.Interval(
                        #     id="interval-component",
                        #     interval=1 * 1000,
                        #     n_intervals=0
                        # ),
                        html.P(className="text-warning",children="Turn the fan > 24"),
                        html.Div([ Gauge.render_gauge(app), Thermometer.render_thermo(app),
                                   html.Img(id="fan_control",className="fan mt-4",src="https://cdn-icons-png.flaticon.com/512/545/545932.png")],
                                 className="d-flex flex-row justify-content-evenly")
                    ],
                )
            ),
        ],

    )

    cardlayout = dbc.Row(
        [
            dbc.Row([
                dbc.Col(profile, width=4),
                dbc.Col(cards, width=8),
            ],)


        ]
    )
    return cardlayout
