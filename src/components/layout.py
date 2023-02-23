# This class is main Layout
# After creating a component ex. the card class, add here as a new div

from dash import Dash, html
# this is the layout manager
# import other components
from src.components import card

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                card.render_card(app)
            )
        ]
    )