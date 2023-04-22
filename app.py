from dash import Dash, html, dcc, Input, Output, callback
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs
from src.Controller.Paho_Broker import ESPBroker
# sqlite import
import asyncio
import sqlite3
from src.Helper import SqLiteDbHelper as dbHelper


# These are the themes
# dbc.themes.VAPOR = this is a cyberpunk theme
# dbc.themes.SLATE = this is a dark faded theme
# dbc.themes.QUARTZ cool gradient

def main() -> None:
    print("Iniating Dashboard...")
    '''
        WHen using Raspberry pi and GPIO
        NOTE: Uncomment this cs.set_up()
        NOTE: Also go to the ControllerSystem.py, uncomment the GPIO.output in the light_controller()
        NOTE: Lastly, uncomment import RPi.GPIO as GPIO and from time import sleep
        
        When you just want to work on the Dashboard, comment out cs.set_up()
    '''
    # setting up the GPIO
    #cs.set_up()

    # start db process
    PATH = 'Database/IoTDatabase.db'
    con = dbHelper.sync_create_connection(PATH)
    #dbHelper.sync_getProfileById(con, "98221647")

    # Setting up the broker
    #broker = ESPBroker("IoTProject/PhotoSensor")
    #broker.start_sub()

    app = Dash(__name__, suppress_callback_exceptions=True,
               update_title=None,
               external_stylesheets=[dbc.themes.QUARTZ])
    app.title = "IOT DashBoard"

    theme_switch = ThemeSwitchAIO(
        aio_id="theme", themes=[dbc.themes.QUARTZ, dbc.themes.SLATE]
    )

    app.layout = dbc.Container(
        [theme_switch,
         html.Div([html.H1(app.title),
                   html.Hr(),
                   html.Div([dcc.Interval(
            id='inteverl_for_url',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
                       dcc.Location(id='url', refresh=False),
                             html.Div(id="page-content", className="container vh-100")
                             ])
                   ]),
         ])

    # -- start pages
    index_page = html.Div([
        html.Div(children=html.Img(src="https://cdn-icons-png.flaticon.com/512/5628/5628131.png"),className="flex-shrink-0")
       ,
        html.Div(
            [
                html.H1("Scan your card"),
                html.H1("to login to your"),
                html.H1("Dashboard"),
                # dcc.Link('Go to Page 1', href='/page-1'),
                # html.Br(),
                # dcc.Link('Go to Page 2', href='/dashboard'),
            ], className="flex-gro-1 ms-3")

    ],className="d-flex align-items-center")

    @callback(
        Output('url','pathname'),
        Input('inteverl_for_url', 'n_intervals')
    )
    def update_login(n):
        asyncio.run(dbHelper.asyncRead(PATH, "675211623"))
        if dbHelper.current_user_data:
            return '/dashboard'
        else:
            return '/'


    # Update the index
    # index callback
    @callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],prevent_initial_call=True)
    def display_page(pathname):
        if pathname is None:
            raise PreventUpdate
        elif pathname == '/':
            return index_page
        elif pathname == '/dashboard':
            return dbc.Container([create_layout(app)])
        # You could also return a 404 "URL not found" page here
    # -- end index callback

    #app.run()
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
