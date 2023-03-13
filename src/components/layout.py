# This class is main Layout
# After creating a component ex. the card class, add here as a new div

from dash import Dash, html
# this is the layout manager
# import other components
from src.components import card
from . import Clock

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="container",
        children=[
            html.H1(app.title),
            #Clock.render_clock(app),
            html.Hr(),
            html.Div(
                card.render_card(app)
            ),

        ]
    )