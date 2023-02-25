from dash import Dash, html
import time
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from src.components.layout import create_layout
import src.Controller.ControllerSystem as cs

# External Javascript
external_scripts = [
    {'src': 'href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"',
     'integrity':"sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4",
     'crossorigin':"anonymous"}
]

# External CSS stylesheets
external_stylesheets = [
    {'href': ''}
]

# dbc.themes.VAPOR = this is a cyberpunk theme
# dbc.themes.SLATE = this is a dark faded theme

def main() -> None:
    app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.SLATE])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)
    print("Iniating Dashboard...")
    # NOTE: Uncomment this if you are using your raspberry pi
    #cs.set_up()

    app.run()


if __name__ == "__main__":
    main()
