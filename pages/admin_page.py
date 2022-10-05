from datetime import datetime
from app import app
import dash
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from my_database import user_information

viscosity_input_table = dbc.Container([
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Label('Tanım'), width={
                    'size': 3}, style={'font-weight': 'bold'}),
            dbc.Col(dbc.Label('Zaman'), width={
                    'size': 3}, style={'font-weight': 'bold'}),
            dbc.Col(dbc.Label('Değer'), width={
                    'size': 3}, style={'font-weight': 'bold'}),
            dbc.Col(dbc.Label('Sıcaklık'), width={
                    'size': 3}, style={'font-weight': 'bold'})
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Input(placeholder='Run X', type='text'), width={'size': 3}
            ),
            dbc.Col(
                dmc.TimeInput(required=True), width={'size': 3}
            ),
            dbc.Col(
                dbc.Input(placeholder='4.2', type='number', min=0, max=100), width={'size': 3}
            ),
            dbc.Col(
                dbc.Input(placeholder='50', type='number', min=20, max=60), width={'size': 3}
            )
        ]),
    ],
        id='viscosity_table'),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Button('Satır Ekle', id='add_row'), width={'size': 'auto', 'order': 'first'}, style={'padding-top': '40px'}
        ),
        dbc.Col(
            dbc.Button('Satır Sil', id='remove_row'), width={'size': 'auto', 'order': 'last'}, style={'padding-top': '40px'}
        )
    ])
])

admin_data_entry_page = dbc.Container([
    dcc.Store(id='new_data_submission'),
    dcc.Store(id='new_data_submission_result'),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id='title_new_data_modal')),
        dbc.ModalBody(id='body_new_data_modal'),
        dbc.ModalFooter(dbc.Button("Close", id="close_new_data_modal")),
    ],
        id="new_data_modal",
        is_open=False,
    ),
    dbc.Row([
        dbc.Col([
            dbc.Alert("Veri alanları boş bırakılamaz.", id="empty-data-field-error", color="danger", is_open=False,
                      dismissable=True)
        ], width="auto")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([dbc.InputGroupText("Deney Adi"),
                            dbc.Select(placeholder='Açık Deneyler',
                                       options=[],
                                       id='code')]),
            html.Br(),
            dbc.InputGroup([dbc.InputGroupText("Teknisyen"), dbc.Input(
                disabled=True, type='text', id='operator')]),
            html.Br(),
            dbc.InputGroup([dbc.InputGroupText("Tarih"),
                           dbc.Input(type='date', id='date')])
        ],
            width={'size': 3}),
        dbc.Col([
            viscosity_input_table],
            style={'border-style': 'solid', 'background-color': 'rgb(196, 196, 196)'}, width={'size': 5, 'offset': 2}
        )], style={'padding-top': '20px'}),
    dbc.Row(
        dbc.Col(
            dbc.Button('Gönder', id='submit_data'), width={'size': 1, 'offset': 11}))
])


@app.callback(
    Output('viscosity_table', 'children'),
    Input('add_row', 'n_clicks'),
    Input('remove_row', 'n_clicks'),
    Input('new_data_submission_result', 'data'),
    State('viscosity_table', 'children'),
    prevent_initial_call=True
)
def formuGüncelle(n_clicks_add, n_clicks_remove, submission, rows):
    if ctx.triggered_id == 'add_row' and n_clicks_add is not None:
        rows.append(
            dbc.Row([
                dbc.Col(
                    dbc.Input(placeholder='Run X', type='text'), width={'size': 3}
                ), dbc.Col(
                    dmc.TimeInput(), width={'size': 3}
                ), dbc.Col(
                    dbc.Input(placeholder='4.2', type='number', min=0, max=100), width={'size': 3}
                ),
                dbc.Col(
                    dbc.Input(placeholder='50', type='number', min=20, max=60), width={'size': 3}
                )
            ])
        )
        return rows
    elif ctx.triggered_id == 'remove_row' and n_clicks_remove is not None:
        if len(rows) > 2:
            rows.pop()
            return rows
        else:
            raise PreventUpdate
    elif ctx.triggered_id == 'new_data_submission_result':
        if submission:
            return [
                dbc.Row([
                    dbc.Col(dbc.Label('Tanım'), width={
                            'size': 3}, style={'font-weight': 'bold'}),
                    dbc.Col(dbc.Label('Zaman'), width={
                            'size': 3}, style={'font-weight': 'bold'}),
                    dbc.Col(dbc.Label('Değer'), width={
                            'size': 3}, style={'font-weight': 'bold'}),
                    dbc.Col(dbc.Label('Sıcaklık'), width={
                            'size': 3}, style={'font-weight': 'bold'})
                ]),
                dbc.Row([
                    dbc.Col(
                        dbc.Input(placeholder='Run X', type='text'), width={'size': 3}
                    ), dbc.Col(
                        dmc.TimeInput(), width={'size': 3}
                    ), dbc.Col(
                        dbc.Input(placeholder='4.2', type='number', min=0, max=100), width={'size': 3}
                    ),
                    dbc.Col(
                        dbc.Input(placeholder='50', type='number', min=20, max=60), width={'size': 3}
                    )
                ]),
            ]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    Output('new_data_submission', 'data'),
    Output("empty-data-field-error", 'is_open'),
    Input('submit_data', 'n_clicks'),
    State('date', 'value'),
    State('viscosity_table', 'children'),
    State('code', 'value'),
    prevent_initial_call=True
)
def veriyiIsle(n_clicks, date, children, code):
    if any([n_clicks is None, date is None, date == '', code is None, code == '']):
        return dash.no_update, True

    df = pd.DataFrame({'Tag': [],
                       'Time': [],
                       'Result': [],
                       'Temperature': []})

    for r, row in enumerate(children):
        if r == 0:
            continue
        else:
            new_row = []

        for c, col in enumerate(row['props']['children']):
            if 'value' in col['props']['children']['props'].keys():
                new_row.append(col['props']['children']['props']['value'])
            else:
                new_row.append(np.nan)

        df.loc[len(df)] = new_row

    if df.isna().sum().sum() != 0:
        return dash.no_update, True

    # Sonuc formundaki zaman kolonu veri girisi yapilan gunu baz almaktadir. Gun degeri operator
    # tarafindan belirtilen manuel tarihe gore duzeltilir.
    date = datetime.strptime(date, '%Y-%m-%d')

    df['Time'] = df['Time'].astype('datetime64[ns]')
    df['Time'] = df['Time'].apply(
        lambda dt: dt.replace(day=date.day, month=date.month))

    return df.to_dict(), False


@app.callback(
    Output('new_data_modal', 'is_open'),
    Output('title_new_data_modal', 'children'),
    Output('body_new_data_modal', 'children'),
    Output('new_data_submission_result', 'data'),
    Input("close_new_data_modal", 'n_clicks'),
    Input('new_data_submission', 'data'),
    State('code', 'value'),
    State('operator', 'value'),
    prevent_initial_call=True
)
def veriyiAktar(close_click, dataFrame, code, operator):
    if ctx.triggered_id == 'close_new_data_modal':
        return False, dash.no_update, dash.no_update, dash.no_update

    sql_response = labDBmanager.obje1.deney_verisi_isle(
        code, operator, pd.DataFrame(dataFrame))

    if sql_response:
        modal_shown = True
        modal_title = 'Deney sonucu alınmıştır.'
        modal_text = 'Deney sonucu sisteme işlenmiştir.'
        sub_result = True
        return modal_shown, modal_title, modal_text, sub_result
    else:
        modal_shown = True
        modal_title = 'Deney sonucu alınamamıştır.'
        modal_text = 'Deney sonucu sisteme işlenememiştir.\nLütfen bütün veri alanlarını doldurduğunuzdan emin olunuz.'
        sub_result = False
        return modal_shown, modal_title, modal_text, sub_result


@app.callback(
    Output("operator", "value"),
    Input("login-control-button", "n_clicks"),
    State("username-box", "value")
)
def setKullaniciAdi(log_click, uname):
    if log_click is None:
        raise PreventUpdate
    else:
        return uname


@app.callback(
    Output('code', 'options'),
    Output('code', 'value'),
    Input('new_data_submission_result', 'data'),
    Input("tabs", "active_tab"),
    prevent_initial_call=True
)
def acikTalepGuncelle(res, activated):
    if (ctx.triggered_id == 'new_data_submission_result' and res) or \
            (ctx.triggered_id == 'tabs' and activated == 'new-data-tab'):
        list_of_open_request = labDBmanager.obje1.deney_talebi_goruntule()
        if list_of_open_request is None:
            return ['Sayfayı yenileyin'], None
        else:
            return [{'label': exp, 'value': exp} for exp in list_of_open_request], None
    else:
        raise PreventUpdate
