# This class is main Layout
# After creating a component ex. the card class, add here as a new div

from dash import Dash, html
# this is the layout manager
# import other components
from src.components import card
from . import Clock
import dash_daq as daq
def create_layout(app: Dash) -> html.Div:
    return html.Div(
        #className="container vh-100",
        children=[
            #html.H1(app.title),
            #Clock.render_clock(app),
            #html.Hr(),
            card.render_card(app)
            # html.Div(id="main_context",
            #     ,
            # )
        ]
    )