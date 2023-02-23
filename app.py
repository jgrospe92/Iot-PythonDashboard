from dash import Dash, html
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs


def main() -> None:
    app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)
    print("Iniating Dashboard...")
    # NOTE: Uncomment this if you are using your raspberry pi
    #cs.set_up()

    app.run()


if __name__ == "__main__":
    main()
