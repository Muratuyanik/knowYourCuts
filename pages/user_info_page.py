from datetime import date, datetime
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from app import app
from my_database import user_information
from dash_extensions import BeforeAfter

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
        ], width="4"),
        dbc.Col([
            dbc.Label("Tarih", html_for="request_submission_date", style={"font-weight": "bold"}),
            dbc.Input(type="date", disabled=True, value=date.today(), id="request_submission_date")
        ], width={"offset": 2, "size": 2})
    ], style={'padding-top': '10px'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Kurumda Ise Baslama Tarihi: ", html_for="corporate_starting_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='corporate_starting_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Sigorta Tarihi",
                date=datetime.now().date(),)
        ], width="4"),
        dbc.Col([
            dbc.Label("Daha Once Calisilan Sure(gun): ", html_for="experience_before", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, min=0, step=1, style={'text-align': 'right'}, id="experience_before"),
        ], width={"offset": 2, "size": 3}),
    ],),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Egitim Durumu", html_for="education_level", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "1": "Lise",
                    "2": "Universite",
                    "3": "Yuksek Lisans",
                    "4": "Doktora"
                }, value="Yok", id="education_level"
            )
        ], width="4"),
        dbc.Col([
            dbc.Label("Mezuniyet Tarihi: ", html_for="graduation_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='graduation_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width={'size': 3, "offset": 2}),
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Medeni Hal", html_for="marriage", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evli', 'Bekar'], 'Bekar', inline=True, id='marriage',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width="4"),
    ], ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Esin Calisma Durumu", html_for="partner", style={"font-weight": "bold"}),
            dcc.RadioItems(['Calismiyor', 'Calisiyor'], 'Calismiyor', inline=True, id='partner',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Baslangic Tarihi: ", html_for="partner_working_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='partner_working_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width={"offset": 2}),
        dbc.Col([
            dbc.Label("Bitis Tarihi: ", html_for="partner_working_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='partner_working_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Suresiz",)
        ], width={"offset": 0})
    ], style={'padding-top': '0px', 'display': 'flex'}, justify='evenly', align='center', id='partner_status'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Cocuk Sayisi", html_for="dependent_childiren", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yok', '1', '2', '3'], 'Yok', inline=True, id='dependent_childiren',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width="4"),
    ], ),
    dbc.Row([
        dbc.Col([
            dbc.Label("1. Cocuk Cinsiyeti", html_for="child_one", style={"font-weight": "bold"}),
            dcc.RadioItems(['Erkek', 'Kiz'], 'Erkek', inline=True, id='child_one',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Dogum tarihi Tarihi: ", html_for="child_one_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_one_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width=3),
        dbc.Col([
            dbc.Label("Bagimli mi", html_for="child_one_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Evet', inline=True, id='child_one_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Engel Durumu", html_for="child_one_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Hayir', inline=True, id='child_one_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_one_status'),
    dbc.Row([
        dbc.Col([
            dbc.Label("2. Cocuk Cinsiyeti", html_for="child_two", style={"font-weight": "bold"}),
            dcc.RadioItems(['Erkek', 'Kiz'], 'Erkek', inline=True, id='child_two',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Dogum tarihi Tarihi: ", html_for="child_two_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_two_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width=3),
        dbc.Col([
            dbc.Label("Bagimli mi", html_for="child_two_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Evet', inline=True, id='child_two_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Engel Durumu", html_for="child_two_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Hayir', inline=True, id='child_two_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_two_status'),
    dbc.Row([
        dbc.Col([
            dbc.Label("3. Cocuk Cinsiyeti", html_for="child_three", style={"font-weight": "bold"}),
            dcc.RadioItems(['Erkek', 'Kiz'], 'Erkek', inline=True, id='child_three',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Dogum tarihi Tarihi: ", html_for="child_three_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_three_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width=3),
        dbc.Col([
            dbc.Label("Bagimli mi", html_for="child_three_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Evet', inline=True, id='child_three_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Engel Durumu", html_for="child_three_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Hayir', inline=True, id='child_three_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_three_status'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Engel Durumu", html_for="disability_level", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "Yok": "Engel Durumu Bulunmuyor",
                    "1": "Birinci Derece(%80+)",
                    "2": "Ikinci Derece(%60-79)",
                    "3": "Ucuncu Derece(%40-59)"
                }, value="Yok", id="disability_level"
            )
        ], width="4"),
        dbc.Col([
            dbc.Label("Baslangic Tarihi: ", html_for="disability_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='disability_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width={"offset": 2}, id='dis_start'),
        dbc.Col([
            dbc.Label("Bitis Tarihi: ", html_for="disability_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='disability_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Suresiz",)
        ], width={"offset": 0}, id='dis_end')
    ], ),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Ozel Saglik Sigortasi", html_for="private_insurance", style={"font-weight": "bold"}),
            dcc.RadioItems(['Var', 'Yok'], 'Yok', inline=True, id='private_insurance',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Sigorta Tarihi: ", html_for="insurance_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='insurance_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Sigorta Tarihi",
                date=datetime.now().date(),)
        ], width={"offset": 2}, id='ins_date'),
        dbc.Col([
            dbc.Label("Toplam Sigorta Tutari: ", html_for="total_insurance", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, min=0, step=0.01, style={'text-align': 'right'}, id="total_insurance"),
        ], id="total_cost"),
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Sendika Uyeligi", html_for="union_membership", style={"font-weight": "bold"}),
            dcc.RadioItems(['Evet', 'Hayir'], 'Hayir', inline=True, id='union_membership',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Baslangic Tarihi: ", html_for="union_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='union_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(),)
        ], width={"offset": 2}, id='union_start'),
        dbc.Col([
            dbc.Label("Bitis Tarihi: ", html_for="union_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='union_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Suresiz",)
        ], width={"offset": 0}, id='union_end')
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Yabanci Dil Puani", html_for="language", style={"font-weight": "bold"}),
            dcc.RadioItems(['Var', 'Yok'], 'Yok', inline=True, id='language',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Sinav Tarihi: ", html_for="exam_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='exam_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Sinav Tarihi",
                date=datetime.now().date(),)
        ], width={"offset": 2}, id="lang_date"),
        dbc.Col([
            dbc.Label("Sinav Puani: ", html_for="exam_score", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, min=0, max=100, step=0.25, style={'text-align': 'right'}, id="exam_score"),
        ], id="lang_score"),
    ]),
    html.Hr(),

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
        ], width={"offset": 3})
    ],),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Calisilan Kurum", html_for="request_submission_date", style={"font-weight": "bold"}),
            dcc.RadioItems(['ILBANK', 'Diger'], 'Diger', inline=True, id='corporation',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button('Kaydet/Guncelle', id='submit_request', style={'background-color': 'rgb(252, 122, 209)'})
            ],
            width={'size': 'auto', 'offset': 9})
        ], style={'padding-top': '40px'})
], style={"border": "1px solid gray", "padding": "10px", 'background-color': 'rgb(225, 224, 156)'},id='submission_form')

user_info_page = dbc.Container([
    dbc.Row([
        dbc.Col([
            request_modals,
            dcc.Store(id='submission_result', data=False),
            request_form
        ], width={"size": 10})
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
        modal_title = 'Bilgileriniz kaydedilmistir.'
        modal_text = 'Kullanici bilgileriniz basarili bir sekilde kaydedilmistir/guncellenmistir.'
        sub_result = True
        return modal_shown, modal_title, modal_text, sub_result
    else:
        modal_shown = True
        modal_title = 'Bilgileriniz kaydedilememistir!'
        modal_text = 'Bilgileriniz kaydedilememistir. Lütfen bilgileriniz kontrol ederek tekrar deneyiniz.'
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


@app.callback(
   Output(component_id='ins_date', component_property='style'),
   Output(component_id='total_cost', component_property='style'),
   [Input(component_id='private_insurance', component_property='value')])

def show_hide_private_insurance(visibility_state):
    if visibility_state == 'Var':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'Yok':
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
   Output(component_id='lang_date', component_property='style'),
   Output(component_id='lang_score', component_property='style'),
   [Input(component_id='language', component_property='value')])

def show_hide_language(visibility_state):
    if visibility_state == 'Var':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'Yok':
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
   Output(component_id='union_start', component_property='style'),
   Output(component_id='union_end', component_property='style'),
   [Input(component_id='union_membership', component_property='value')])

def show_hide_union(visibility_state):
    if visibility_state == 'Evet':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'Hayir':
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
   Output(component_id='dis_start', component_property='style'),
   Output(component_id='dis_end', component_property='style'),
   [Input(component_id='disability_level', component_property='value')])

def show_hide_disability(visibility_state):
    if visibility_state != 'Yok':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'Yok':
        return {'display': 'none'}, {'display': 'none'}

@app.callback(
   Output(component_id='partner_status', component_property='style'),
   [Input(component_id='marriage', component_property='value')])

def show_hide_partner(visibility_state):
    if visibility_state == 'Evli':
        return {'display': 'flex'}
    if visibility_state == 'Bekar':
        return {'display': 'none'}

@app.callback(
   Output(component_id='child_one_status', component_property='style'),
   Output(component_id='child_two_status', component_property='style'),
   Output(component_id='child_three_status', component_property='style'),
   [Input(component_id='dependent_childiren', component_property='value')])

def show_hide_children(visibility_state):
    if visibility_state == 'Yok':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    if visibility_state == '1':
        return {'display': 'flex'}, {'display': 'none'}, {'display': 'none'}
    if visibility_state == '2':
        return {'display': 'flex'}, {'display': 'flex'}, {'display': 'none'}
    if visibility_state == '3':
        return {'display': 'flex'}, {'display': 'flex'}, {'display': 'flex'}