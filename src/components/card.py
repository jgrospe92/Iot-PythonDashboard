# This is a sample of a component class
import time
import dash_bootstrap_components as dbc
from dash import html, Dash
from dash.dependencies import Input, Output
import src.Controller.ControllerSystem as cs
import dash_daq as daq
from . import Colors


def render_card(app: Dash) -> html.Div:
    # Add the callbacks
    # Callbacks for the button switch
    @app.callback(
        # Output(component_id='btn-activate', component_property='children'),
        # Input(component_id='btn-activate', component_property='n_clicks'),
        Output(component_id='lightbulb', component_property="style"),
        Input('our-power-button-1', 'on'),
    )
    def update_button(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        else:
            # Tenary operator return OFF if condiion is == 0 else ON
            return {'background-color': '#000'} if cs.light_controller() == 0 else {'background-color': '#FFDB12'}

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
                        html.H5("LED CONTROL", className="card-title"),
                        html.P(
                            "Turn the switch on or off.",
                            className="card-text",
                        ),
                        html.Div([
                            daq.PowerButton(
                                id='our-power-button-1',
                                on=True,
                                size=100,
                                color=Colors.GREEN
                            ),
                            html.Div(id='power-button-result-1'),
                            html.Div(id="lightbulb", className="light-off"),
                        ],className="d-flex flex-row justify-content-evenly"),
                    ],className=""
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Fan Status", className="card-title"),
                        html.P(className="text-warning",children="add fan gadget here"),
                        html.Div(style={"display": "flex", " align-items": "center", "justify-content": "center",
                                        }, children=html.Div(id="", className="mx-4")),
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
            ],className="")


        ]
    )
    return cardlayout
