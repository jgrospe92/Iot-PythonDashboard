from dash import Dash, html
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs


# These are the themes
# dbc.themes.VAPOR = this is a cyberpunk theme
# dbc.themes.SLATE = this is a dark faded theme

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

    app = Dash(__name__, update_title=None, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.VAPOR])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)

    app.run()


if __name__ == "__main__":
    main()