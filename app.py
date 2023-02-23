from dash import Dash, html
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout



# Import RPi and time libraris
# Temporary disabled these libraries / uncomment it if you are using your Raspberry pi
# import RPi.GPIO as GPIO
# from time import sleep

def main() -> None:
    app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)
    # NOTE: Uncomment this if you are using your raspberry pi
    #cs.set_up()

    app.run()


if __name__ == "__main__":
    main()
