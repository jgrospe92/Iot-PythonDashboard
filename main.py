from dash import Dash, html, Input, Output
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs


# Import RPi and time libraris
# Temporary disabled these libraries / uncomment it if you are using your Raspberry pi
# import RPi.GPIO as GPIO
# from time import sleep

def main() -> None:
    app = Dash(external_stylesheets=[dbc.themes.SLATE])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)

    # NOTE: Uncomment this if you are using your raspberry pi
    #cs.set_up()

    # Button Callbacks
    @app.callback(
        Output(component_id='btn-activate', component_property='children'),
        Input(component_id='btn-activate', component_property='n_clicks')
    )
    def update_output(n_clicks):
        global isActive
        if n_clicks is None:
            raise PreventUpdate
        else:
            # Tenary operator return OFF if condiion is == 0 else ON
            return "OFF" if cs.light_controller() == 0 else "ON"

    app.run()


if __name__ == "__main__":
    main()
