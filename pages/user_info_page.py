from datetime import date
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from app import app
from my_database import user_information


request_modals = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id='title_request_modal')),
            dbc.ModalBody(id='body_request_modal'),
            dbc.ModalFooter(dbc.Button("Close", id="close_request_modal")),
            ],
            id="request_modal",
            is_open=False,
            )

request_form = dbc.Form([
    dbc.Row([
        dbc.Col([
            dbc.Label("Kullanıcı Adı", html_for="request_user", style={"font-weight": "bold"}),
            dbc.Input(type="text", disabled=True, id="request_user")
        ]),
        dbc.Col([
            dbc.Label("Tarih", html_for="request_submission_date", style={"font-weight": "bold"}),
            dbc.Input(type="date", disabled=True, value=date.today(), id="request_submission_date")
        ], width={"offset": 4})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Deney Kafilesi", html_for="request_exp_name", style={"font-weight": "bold"}),
            dbc.Input(type="text", id="request_exp_name"),
        ]),
        dbc.Col([
            dbc.Label("Deney Türü", html_for="request_exp_type", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "A": "A Tipi Kültür",
                    "B": "B Tipi Kültür"
                }, id="request_exp_type"
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button('Kaydet/Guncelle', id='submit_request')
        ], width={'size': 'auto', 'offset': 9})
    ], style={'padding-top': '10px'})
], style={"border": "1px solid gray", "padding": "10px", 'background-color': 'rgb(196, 196, 196)'}, id='submission_form')

user_info_page = dbc.Container([
    dbc.Row([
        dbc.Col([
            request_modals,
            dcc.Store(id='submission_result', data=False),
            request_form
        ], width={"size": 8})
    ], justify="center")
], style={"padding-top": "50px"})

@app.callback(
    Output('request_modal', 'is_open'),
    Output('title_request_modal', 'children'),
    Output('body_request_modal', 'children'),
    Output('submission_result', 'data'),
    Input('submit_request', 'n_clicks'),
    Input('close_request_modal', 'n_clicks'),
    State('request_user', 'value'),
    State("request_submission_date", 'value'),
    State("request_exp_name", 'value'),
    State("request_exp_type", 'value'),
    prevent_initial_call=True
)
def talebiIsle(sub_click, modal_click, uname, sub_date, exp_name, exp_type):
    if ctx.triggered_id == 'close_request_modal':
        return False, dash.no_update, dash.no_update, dash.no_update

    data_dict = {'kullaniciAdi': uname,
                 'talepTarihi': sub_date,
                 'deneyKafilesi': exp_name,
                 'deneyTipi': exp_type}

    if None in data_dict.values() or '' in data_dict.values():
        raise PreventUpdate

    sql_response, request_ID = labDBmanager.obje1.deney_talebi_isle(data_dict['kullaniciAdi'],
                                                                    data_dict['deneyTipi'],
                                                                    data_dict['deneyKafilesi'],
                                                                    data_dict['talepTarihi'])

    if sql_response:
        modal_shown = True
        modal_title = 'Deney talebiniz alınmıştır.'
        modal_text = 'Deney talebiniz laboratuvara iletilmiştir.\nTalep numaranız {}\'dır.'.format(request_ID)
        sub_result = True
        return modal_shown, modal_title, modal_text, sub_result
    else:
        modal_shown = True
        modal_title = 'Deney talebiniz alınamamıştır!'
        modal_text = 'Deney talebiniz alınamamıştır. Lütfen bütün alanları doldurduğunuzu kontrol ediniz.'
        sub_result = False
        return modal_shown, modal_title, modal_text, sub_result

@app.callback(
    Output('submission_form', 'children'),
    Input('submission_result', 'data')
)
def tabloyuSifirla(response):
    if response:
        return [
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Kullanıcı Adı", html_for="request_user", style={"font-weight": "bold"}),
                        dbc.Input(type="text", disabled=True, id="request_user")
                    ]),
                    dbc.Col([
                        dbc.Label("Tarih", html_for="request_submission_date", style={"font-weight": "bold"}),
                        dbc.Input(type="date", disabled=True, value=date.today(), id="request_submission_date")
                    ], width={"offset": 4})
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Deney Kafilesi", html_for="request_exp_name", style={"font-weight": "bold"}),
                        dbc.Input(type="text", id="request_exp_name"),
                    ]),
                    dbc.Col([
                        dbc.Label("Deney Türü", html_for="request_exp_type", style={"font-weight": "bold"}),
                        dcc.Dropdown(
                            options={
                                "A": "A Tipi Kültür",
                                "B": "B Tipi Kültür"
                            }, id="request_exp_type"
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Gönder', id='submit_request')
                    ], width={'size': 'auto', 'offset': 10})
                ], style={'padding-top': '10px'})
                ]
    else:
        return dash.no_update


@app.callback(
    Output("request_user", "value"),
    Input("login-control-button", "n_clicks"),
    State("username-box", "value")
)
def setKullaniciAdi(log_click, uname):
    if log_click is None:
        raise PreventUpdate
    else:
        return uname
