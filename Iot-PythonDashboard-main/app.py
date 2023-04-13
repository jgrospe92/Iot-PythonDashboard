from dash import Dash, html
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs
from src.Controller.Paho_Broker import ESPBroker



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

    # Setting up the broker
    #broker = ESPBroker("IoTProject/PhotoSensor")
    #broker.start_sub()

    app = Dash(__name__, update_title=None, external_stylesheets=[dbc.themes.QUARTZ])
    app.title = "IOT DashBoard"
    theme_switch = ThemeSwitchAIO(
        aio_id="theme", themes=[dbc.themes.QUARTZ, dbc.themes.VAPOR]
    )

    app.layout = dbc.Container([theme_switch,create_layout(app)])

    app.run()


if __name__ == "__main__":
    main()
