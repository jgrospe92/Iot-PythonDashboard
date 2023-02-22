import dash_bootstrap_components as dbc
from dash import html, Dash


def render_card(app: Dash) -> html.Div:
    cards = dbc.CardGroup(
        [
            dbc.Card([
                dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/560/560277.png",
                            top=True,
                            style={"width":"10rem",
                                   "border-radius": "50%",
                                   "align-self":"center",
                                   "justify-self": "center"}),

                dbc.CardBody(
                    [
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
                            "Click here", color="success", className="mt-auto"
                        ),
                    ]
                )
            ],

            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Controll System", className="card-title"),
                        html.P(
                            "Turn the switch on or off.",
                            className="card-text",
                        ),
                        dbc.Button(
                            "ON", color="success", className="mt-auto"
                        ),
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5("Status", className="card-title"),
                        html.P(
                            "TODO: add image or css styling for the light",
                            className="card-text",
                        ),
                        # dbc.Button(
                        #     "Click here", color="danger", className="mt-auto"
                        # ),
                    ]
                )
            ),
        ]
    )
    return cards
