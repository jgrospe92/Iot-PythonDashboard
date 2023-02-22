from dash import Dash, html
# from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from src.components.layout import  create_layout


def main() ->None:
    app = Dash(external_stylesheets=[dbc.themes.SLATE])
    app.title = "IOT DashBoard"
    app.layout = create_layout(app)
    app.run()

if __name__ == "__main__":
    main()