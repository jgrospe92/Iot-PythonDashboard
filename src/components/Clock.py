import dash_daq as daq
from dash import html, Dash
from datetime import datetime


def render_clock(app: Dash) -> html.Div:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return daq.LEDDisplay(
        value=current_time,
        size=20,
    )