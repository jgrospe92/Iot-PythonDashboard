import dash_daq as daq
from dash import html, Dash, dcc
from datetime import datetime
from dash.dependencies import Input, Output


def render_clock(app: Dash) -> html.Div:
    @app.callback(Output("time", "value"),Input("clock", "n_intervals"))
    def update_time(n):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return  current_time

    return html.Div([daq.LEDDisplay(id="time",
                color="#DE04A3",
                backgroundColor="#1A0933",
                value='0'),dcc.Interval(id="clock", interval=1000, n_intervals=0)])

# def render_clock(app: Dash) -> html.Div:
#     @app.callback(
#         Output("time_update", 'children'),
#         Input("clock", "n_intervals"),
#     )
#     def update_time(n):
#         now = datetime.now()
#         current_time = now.strftime("%H:%M:%S")
#         return current_time
#
#
#    time_now = html.Div([html.H1(id="date-time"),
#         dcc.Interval(id="clock", interval=1000, n_intervals=0)])

#     return time_now
