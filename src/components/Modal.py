import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, Dash


def render_modal(app: Dash):
    @app.callback(
        Output("modal-dismiss", "is_open"),
        [Input("open-dismiss", "n_clicks"), Input("close-dismiss", "n_clicks")],
        [State("modal-dismiss", "is_open")],
    )
    def toggle_modal(n_open, n_close, is_open):
        if n_open or n_close:
            return not is_open
        return is_open

    return html.Div(
        [
            dbc.Button(children="Logout", id="open-dismiss", className="mt-2 btn btn-warning btn-sm"),
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        dbc.ModalTitle("Log out"), close_button=False
                    ),
                    dbc.ModalBody(
                        "Are you sure you want to logout?"
                    ),
                    dbc.ModalFooter([dbc.Button("Yes", id="close-dismiss", href="/"), dbc.Button("No", id="close-dismiss")]),

                ],
                id="modal-dismiss",
                keyboard=False,
                backdrop="static",
            ),
        ],
    )
