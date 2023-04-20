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
import src.Helper.SqLiteDbHelper as dbHelper


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

    #cs.set_up()

    # start db process

    dbHelper.create_connection()
    dbHelper.sync_read()

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

    # app.layout = dbc.Container([theme_switch,create_layout(app)])
    # app.layout = html.Div([
    #     dcc.Location(id='url', refresh=False),
    #     html.Div(id='page-content')
    # ])
    app.layout = dbc.Container(
        [theme_switch,
         html.Div([html.H1(app.title),
                   html.Hr(),
                   html.Div([dcc.Location(id='url', refresh=False),
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
                dcc.Link('Go to Page 1', href='/page-1'),
                html.Br(),
                dcc.Link('Go to Page 2', href='/dashboard'),
            ], className="flex-gro-1 ms-3")

    ],className="d-flex align-items-center")

    # pages
    dashboard_layout = dbc.Container([create_layout(app)])

    page_1_layout = html.Div([
        html.H1('Page 1'),
        dcc.Dropdown(['LA', 'NYC', 'MTL'], 'LA', id='page-1-dropdown'),
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to Page 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go back to home', href='/'),
    ])
    @callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
    def page_1_dropdown(value):
        return f'You have selected {value}'

    page_2_layout = html.Div([
        html.H1('Page 2'),
        dcc.RadioItems(['Orange', 'Blue', 'Red'], 'Orange', id='page-2-radios'),
        html.Div(id='page-2-content'),
        html.Br(),
        dcc.Link('Go to Page 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ])

    @callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
    def page_2_radios(value):
        return f'You have selected {value}'

    # Update the index
    @callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/page-1':
            return page_1_layout
        elif pathname == '/dashboard':
            return dashboard_layout
        else:
            return index_page
        # You could also return a 404 "URL not found" page here
    # -- end test


    app.run_server(debug=True)


if __name__ == "__main__":
    main()
