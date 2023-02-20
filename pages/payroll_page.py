import json

import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_bootstrap_components as dbc
from app import app
from main_wage import Wage
from my_database import user_information
from datetime import datetime, date

from payroll import Payroll

df_of_results = pd.DataFrame({})

payroll_modals = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id='title_payroll_modal')),
    dbc.ModalBody(id='body_payroll_modal'),
    dbc.ModalFooter(dbc.Button("Close", id="close_payroll_modal")),
],
    id="payroll_modal",
    is_open=False,
)

payroll_details = dbc.Form([
    dcc.Store(id='calculated_payroll_data'),
    dbc.Row([
        dbc.Col([
            dbc.Label("BORDRO DETAYLARI", html_for="higher_education", className='h2 secondary'),
        ], className='d-flex justify-content-center secondary')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("ODEME TURU: ", html_for="title_payment_type"),
            html.Output(id="title_payment_type", className='text-uppercase'),
        ], className="col-3"),
        dbc.Col([
            dbc.Label("ODEME TARIHI: ", html_for="title_payment_date"),
            html.Output(id="title_payment_date"),
        ]),
        dbc.Col([
            dbc.Label("KUM VERGI MATRAHI: ", html_for="cumulative_tax_base"),
            html.Output(id="cumulative_tax_base"),
        ], className="ms-auto text-end")
    ], className='fw-bold fs-5 d-flex flex-row border border-3 border-primary bg-warning text-white'),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Label("Temel Ucret: ", html_for="base_wage", className='col-9'),
                html.Output(id="base_wage", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Ust Ogrenim Tazminati: ", html_for="higher_education", className='col-9'),
                html.Output(id="higher_education", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Kidem Primi: ", html_for="seniority_bonus", className='col-9'),
                html.Output(id="seniority_bonus", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Dil Tazminati: ", html_for="language_bonus", className='col-9'),
                html.Output(id="language_bonus", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Fazla Calisma (Saat): ", html_for="overtime", className='col-9'),
                html.Output(id="overtime", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Fazla Calisma Ucreti: ", html_for="overtime_pay", className='col-9'),
                html.Output(id="overtime_pay", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Toplu Sozlesme Ucreti: ", html_for="union_bonus", className='col-9'),
                html.Output(id="union_bonus", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Aile Yardimi: ", html_for="family_support", className='col-9'),
                html.Output(id="family_support", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Brut Maas: ", html_for="gross_wage", className='col-9'),
                html.Output(id="gross_wage", className='col-3 text-end')
            ], className="fw-bold fs-3 bg-secondary text-white justify-content-between mt-auto"),
        ], className="border border-3 border-primary d-flex flex-column"),
        dbc.Col([
            dbc.Row([
                dbc.Label("SSK Matrah: ", html_for="social_security_base", className='col-9'),
                html.Output(id="social_security_base", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("SSK Devir: ", html_for="insurance_turnover", className='col-9'),
                html.Output(id="insurance_turnover", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("SSK Primi: ", html_for="insurance_premium", className='col-9'),
                html.Output(id="insurance_premium", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Issizlik Primi: ", html_for="unemployment_premium", className='col-9'),
                html.Output(id="unemployment_premium", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Engellilik Vergi Indirimi: ", html_for="disability_discount", className='col-9'),
                html.Output(id="disability_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Ozel Sigorta Vergi Indirimi: ", html_for="private_insurance_discount", className='col-9'),
                html.Output(id="private_insurance_discount", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Sendika Vergi Indirimi: ", html_for="union_discount", className='col-9'),
                html.Output(id="union_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Toplam Vergi Indirimi: ", html_for="total_tax_discount", className='col-9'),
                html.Output(id="total_tax_discount", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Gelir Vergisi Matrahi: ", html_for="income_tax_base", className='col-9'),
                html.Output(id="income_tax_base", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Gelir Vergisi: ", html_for="income_tax", className='col-9'),
                html.Output(id="income_tax", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Asgari Ucret Vergi Indirimi: ", html_for="minimum_wage_discount", className='col-9'),
                html.Output(id="minimum_wage_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Odenecek Gelir Vergisi: ", html_for="tax_to_pay", className='col-9'),
                html.Output(id="tax_to_pay", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Damga Vergisi: ", html_for="stamp_duty", className='col-9'),
                html.Output(id="stamp_duty", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Toplam Yasal Kesintiler: ", html_for="total_legal_cuts", className='col-9'),
                html.Output(id="total_legal_cuts", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Net Maas: ", html_for="net_income", className='col-9'),
                html.Output(id="net_income", className='col-3 text-end')
            ], className="fw-bold fs-3 bg-secondary text-white justify-content-between mt-auto"),
        ], className="border border-3 border-primary d-flex flex-column"),
    ], className="border border-3 border-primary"),
], style={'padding-top': '30px'}, id="payroll_detail")

payroll_calculation = dbc.Container([
    dcc.Store(id='current-data'),
    dcc.Store(id='data-loaded', data=False),
    dcc.Download(id="download-dataframe-csv"),
    dbc.Row([
        dbc.Col([
            dbc.Label("Odeme Yapilacak Tarih: ", html_for="payment-date-div"),
            dash.html.Div(
                dcc.DatePickerSingle(
                    id='payment_date',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2050, 9, 19),
                    clearable=True,
                    initial_visible_month=datetime.now().date(),
                    date=datetime.now().date(),

                ), id="payment-date-div", className="w-100")
        ], className='col-2'),
        dbc.Col([
            dbc.Label("Odeme Turu:", html_for="payment_type"),
            dcc.Dropdown(
                options={
                    "wage": "Maas",
                    "premium": "Ikramiye",
                    "dividend": "Kontrolluk/Temmettu",
                    "wage_disparity": "Maas Farki"
                }, value="wage", id="payment_type"
            ),
        ], className='col-2'),
        dbc.Col([
            dbc.Label("Odeme Katsayisi:", html_for="payment_compound"),
            dbc.Input(type="number", value=1, min=0, max=100, step=0.01,
                      id="payment_compound"),
        ], id="compound", className='col-2'),
        dbc.Col([
            dbc.Label("Fazla Calisma(saat):", html_for="overtime_hour"),
            dbc.Input(type="number", value=0, min=0, max=55, step=1,
                      id="overtime_hour"),
        ], id="overtime_component", className='col-2'),
        dbc.Col([
            dbc.Button('Hesapla', id='calculate_payroll', className="btn btn-success"),
        ], className="align-self-end mb-2 col-2 offset-1"),
        dbc.Col([
            dbc.Button('Kaydet', id='save_payroll', className="btn btn-warning"),
        ], className="align-self-end mb-2 col-2")
    ]),
])

payroll_graph = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                options=[], placeholder="Odeme Tarihi Seçiniz.",
                multi=True, id="result-list-picker"
            ),
            html.Br(),
            dbc.Button('İndir', id='download-raw-data-button', color="success")
        ], width={"size": 3, "order": "first"}),
        dbc.Col(
            dcc.Graph(id='result-graph')
        ),
        dbc.Col(
            dbc.Table([[], []], bordered=True, hover=True, responsive=True, id='result-table')
        ),
    ], justify='between', style={'padding-top': '50px'}),
])

payroll_page = dbc.Container([
    payroll_modals,
    dbc.Row([
        payroll_calculation
    ]),
    dbc.Row([
        payroll_details
    ]),
    dbc.Row([
        payroll_graph
    ]),
], style={'padding-top': '20px'})


@app.callback(
    Output('calculated_payroll_data', 'data'),
    Output('title_payment_type', 'children'),
    Output("title_payment_date", "children"),
    Output("cumulative_tax_base", "children"),

    Output("base_wage", "children"),
    Output("higher_education", "children"),
    Output("seniority_bonus", "children"),
    Output("language_bonus", "children"),
    Output("overtime", "children"),
    Output("overtime_pay", "children"),
    Output("union_bonus", "children"),
    Output("family_support", "children"),
    Output("gross_wage", "children"),

    Output("social_security_base", "children"),
    Output("insurance_turnover", "children"),
    Output("insurance_premium", "children"),
    Output("unemployment_premium", "children"),
    Output("disability_discount", "children"),
    Output("private_insurance_discount", "children"),
    Output("union_discount", "children"),
    Output("total_tax_discount", "children"),
    Output("income_tax_base", "children"),
    Output("income_tax", "children"),
    Output("minimum_wage_discount", "children"),
    Output("tax_to_pay", "children"),
    Output("stamp_duty", "children"),
    Output("total_legal_cuts", "children"),
    Output("net_income", "children"),
    Input('calculate_payroll', 'n_clicks'),
    State("user-id", "data"),
    State("payment_date", "date"),
    State("payment_type", "value"),
    State("overtime_hour", "value"),
    State("payment_compound", "value")
)
def calculate_payroll(calculate, user_id, p_date, p_type, overtime, compound):
    year, month, day = p_date.split('-')
    payment_date = datetime(int(year), int(month), int(day)).date()
    t_dict = {"wage": "Maas", "premium": "Ikramiye", "dividend": "Kontrolluk/Temmettu","wage_disparity": "Maas Farki"}
    if calculate is None:
        raise PreventUpdate
    else:
        payroll = Wage(user_id, p_type, payment_date, compound, overtime)
        p_dict = payroll.payroll_dict
        print(payroll.payroll_dict)
        print("************Calculated***********")
        # df = pd.DataFrame(payroll.payroll_dict, index={payroll.payroll_dict['payment_type']})    // converting to df
        overtime = p_dict["overtime"] if 'overtime' in p_dict.keys() else 0
        overtime_pay = p_dict["overtime_pay"] if 'overtime_pay' in p_dict.keys() else 0
        union_bonus = p_dict["union_bonus"] if 'union_bonus' in p_dict.keys() else 0

    return p_dict, t_dict[p_type], p_date, p_dict["cumulative_tax_base"],\
           p_dict["base_wage"], p_dict["higher_education_compensation"], p_dict["seniority_bonus"], \
           p_dict["language_compensation"], overtime, overtime_pay, union_bonus, p_dict["family_support"], \
           p_dict["gross_wage"], p_dict["gross_wage"], p_dict["ins_pre_turnover"], p_dict["insurance_premium"], \
           p_dict["unemployment_premium"], p_dict["disability_discount"], p_dict["private_insurance"], \
           p_dict["union_discount"], p_dict["total_tax_discount"], p_dict["income_tax_base"], p_dict["income_tax"],\
           p_dict["minimum_wage_discount"], p_dict["tax_to_pay"], p_dict["stamp_duty"], \
           p_dict["total_legal_cuts"], p_dict["net_income"]

@app.callback(
    Output('payroll_modal', 'is_open'),
    Output('title_payroll_modal', 'children'),
    Output('body_payroll_modal', 'children'),
    Input('save_payroll', 'n_clicks'),
    Input('close_payroll_modal', 'n_clicks'),
    State("user-id", "data"),
    State('calculated_payroll_data', 'data'),
)
def show_payroll(save_click, modal_click, user_id, data_dict):
    if None in data_dict.values() or '' in data_dict.values():
        raise PreventUpdate
    print(data_dict)
    payroll = Payroll(user_id)
    # sql_response = payroll.insert_payroll(data_dict)
    # print(data_dict)
    # print(sql_response)
    # if sql_response:
    #     modal_shown = True
    #     modal_title = 'Bilgileriniz kaydedilmistir.'
    #     modal_text = 'Kullanici bilgileriniz basarili bir sekilde kaydedilmistir/guncellenmistir.'
    #     sub_result = True
    #     return modal_shown, modal_title, modal_text, sub_result
    # else:
    #     modal_shown = True
    #     modal_title = 'Bilgileriniz kaydedilememistir!'
    #     modal_text = 'Bilgileriniz kaydedilememistir. Lütfen bilgileriniz kontrol ederek tekrar deneyiniz.'
    #     sub_result = False
    #     return modal_shown, modal_title, modal_text, sub_result

@app.callback(
    Output("result-table", "children"),
    Output('result-graph', 'figure'),
    Output('current-data', 'data'),
    Input("result-list-picker", "value"),
    prevent_initial_call=True
)
def sonuclariGoster(experiment_list):
    if len(experiment_list) == 0:
        empty_graph = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                                 font=dict(family="sans serif", size=25, color="crimson"),
                                                 showarrow=False, yshift=10)
        return None, empty_graph, {}

    global df_of_results
    df_of_results_filtered = df_of_results[df_of_results['talepID'].isin(experiment_list)].sort_values(by=['talepID',
                                                                                                           'zaman'])
    # Table formati
    table_header = [html.Thead(html.Tr([html.Th(column) for column in df_of_results_filtered.columns]))]
    table_body = [html.Tbody([html.Tr([html.Td(data) for data in row])
                              for index, row in df_of_results_filtered.iterrows()])]
    # Graph formati
    try:
        dateCol = df_of_results_filtered.groupby('talepID').apply(normalizeToKS)['zaman']
        dateCol = dateCol / np.timedelta64(1, 'h')
        mergedDF = df_of_results_filtered.merge(dateCol, how='inner', left_index=True, right_index=True)
    except:
        print('Dataframe time corruption occured.')
        raise PreventUpdate
    graph = px.line(mergedDF, x='zaman_y', y='sonuc', text='aciklama', color='talepID', hover_name="talepID",
                    hover_data={"zaman_y": False, "sicaklik": True, "sonuc": True, "talepID": False, "aciklama": False})
    graph.update_traces(textposition="bottom right")
    graph.update_layout(hovermode="x unified")
    return table_header + table_body, graph, df_of_results_filtered.to_dict()


@app.callback(
    Output('result-list-picker', 'options'),
    Output('data-loaded', 'data'),
    Input("tabs", "active_tab"),
    State('data-loaded', 'data'),
    prevent_initial_call=True
)
def deneySonucuGuncelle(activated, loaded):
    if activated == "query-tab" and not (loaded):
        try:
            global df_of_results
            df_of_results = labDBmanager.obje1.deney_sonucu_goruntule()
            list_of_results = df_of_results.loc[:, 'talepID'].unique()

            if list_of_results is None:
                print("Veriler yüklenemedi.")
                raise PreventUpdate
            else:
                print("Veriler yüklendi.")
                return list_of_results, True

        except:
            print("Veriler yüklenemedi.")
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('download-raw-data-button', 'n_clicks'),
    State('current-data', 'data'),
    prevent_initial_call=True
)
def hamVeri_indir(click, data):
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "Result_{}.csv".format(int(datetime.now().timestamp())))


def normalizeToKS(group):
    # KS bilgisinin bulundugu deney gruplarinda olcumlerin zaman degerleri KS bolgeleri 0 kabul edilerek bagil degerler
    # atanacaktir.
    # KS bilgisinin bulunmadigi deneylerde ise ilk olcum zamani KS sayilacaktir.
    try:
        group['zaman'] = group['zaman'] - group[group['aciklama'].str.upper() == 'KS']['zaman'].iloc[0]
    except:
        group['zaman'] = group['zaman'] - group['zaman'].min()
    return group


@app.callback(
    Output('compound', 'style'),
    Output("overtime_component", "style"),
    [Input('payment_type', 'value')])
def show_hide_payment_compound(visibility_state):
    if visibility_state == 'wage':
        return {'display': 'none'}, {'display': 'block'}
    else:
        if visibility_state == 'dividend':
            return {'display': 'block'}, {'display': 'none'}
        else:
            return {'display': 'none'}, {'display': 'none'}
