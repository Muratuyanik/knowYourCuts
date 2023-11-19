import dash
from dash import html, Input, Output, State, ctx, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import users
from app import app

# dash.register_page(__name__)   # update dash

login_page = dbc.Container([
    dcc.Store(id="user-id"),
    dbc.Row([
        dbc.Col([
            dbc.Alert("Invalid username or password", id="login-error-alert",
                      color="danger", is_open=False, dismissable=True)
        ], width="auto")
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            dbc.Label("User Name"),
            dbc.Input(type="text", id="username-box")
        ], width={"size": "auto"})
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Password"),
            dbc.Input(type="password", id="password-box")
        ], width="auto")
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dbc.Button("Sign In", id="login-control-button", color="success")
        ], width={"size": "auto", "offset": "2"})
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dbc.Button("Sign Up", id="register-button", color="warning")
        ], width={"size": "auto", "offset": "2"})
    ], justify="center"),
])


@app.callback(
    Output("user-info-tab", "disabled"),
    Output("payroll-tab", "disabled"),
    Output("payroll-graphs-tab", "disabled"),
    Output("logout-tab", "disabled"),
    Output("admin-data-entry-tab", "disabled"),
    Output("login-tab", "disabled"),
    Output("tabs", "active_tab"),
    Output("login-error-alert", "is_open"),
    Output("user-id", "data"),
    Input("login-control-button", "n_clicks"),
    Input("tabs", "active_tab"),
    State("username-box", "value"),
    State("password-box", "value"),
    prevent_initial_call=True
)
def authorization_check(n_clicks, tab, uname, password):
    if ctx.triggered_id == "login-control-button":
        if n_clicks is None:
            raise PreventUpdate

        user = users.Users()
        sql_response = user.sign_in(uname, password)
        if sql_response is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
                   "login-tab", True, None
        else:
            permission_level = sql_response[0]
            user_id = sql_response[1]

            if permission_level == "admin":
                return False, False, False, False, False, True, "admin-data-entry-tab", False, user_id
            elif permission_level == "user":
                return False, False, False, False, dash.no_update, True, "user-info-tab", dash.no_update, user_id
            else:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                       dash.no_update, True, None

    if ctx.triggered_id == "tabs" and tab == "logout-tab":
        return True, True, True, True, True, False, "login-tab", False, None

    raise PreventUpdate
