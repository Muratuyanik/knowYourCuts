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

saved_payrolls = pd.DataFrame({})


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
            dbc.Label("Payroll Details", html_for="higher_education", className='h2 secondary'),
        ], className='d-flex justify-content-center secondary')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Label("Payment Date: ", html_for="title_payment_date"),
            html.Output(id="title_payment_date"),
        ], className="col-3"),
        dbc.Col([
            dbc.Label("Payment Type: ", html_for="title_payment_type"),
            html.Output(id="title_payment_type", className='text-uppercase'),
        ]),
        dbc.Col([
            dbc.Label("Cumulative Tax Base: ", html_for="cumulative_tax_base"),
            html.Output(id="cumulative_tax_base"),
        ], className="ms-auto text-end")
    ], className='fw-bold fs-5 d-flex flex-row border border-3 border-primary bg-warning text-info'),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Label("Base Wage: ", html_for="base_wage", className='col-9'),
                html.Output(id="base_wage", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Higher Education Compensation: ", html_for="higher_education", className='col-9'),
                html.Output(id="higher_education", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Seniority Bonus: ", html_for="seniority_bonus", className='col-9'),
                html.Output(id="seniority_bonus", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Language Compensation: ", html_for="language_bonus", className='col-9'),
                html.Output(id="language_bonus", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Overtime (Hour): ", html_for="overtime", className='col-9'),
                html.Output(id="overtime", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Overtime Payment: ", html_for="overtime_pay", className='col-9'),
                html.Output(id="overtime_pay", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Union Bonus: ", html_for="union_bonus", className='col-9'),
                html.Output(id="union_bonus", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Family Support: ", html_for="family_support", className='col-9'),
                html.Output(id="family_support", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Gross Wage: ", html_for="gross_wage", className='col-9'),
                html.Output(id="gross_wage", className='col-3 text-end')
            ], className="fw-bold fs-3 bg-secondary text-white justify-content-between mt-auto"),
        ], className="border border-3 border-primary d-flex flex-column"),
        dbc.Col([
            dbc.Row([
                dbc.Label("Social Security Base: ", html_for="social_security_base", className='col-9'),
                html.Output(id="social_security_base", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("SS Turnover: ", html_for="insurance_turnover", className='col-9'),
                html.Output(id="insurance_turnover", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("SS Cut: ", html_for="insurance_premium", className='col-9'),
                html.Output(id="insurance_premium", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Unemployment Cut: ", html_for="unemployment_premium", className='col-9'),
                html.Output(id="unemployment_premium", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Disability Discount: ", html_for="disability_discount", className='col-9'),
                html.Output(id="disability_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Private Insurance Discount: ", html_for="private_insurance_discount", className='col-9'),
                html.Output(id="private_insurance_discount", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Union Discount: ", html_for="union_discount", className='col-9'),
                html.Output(id="union_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Total Tax Discount: ", html_for="total_tax_discount", className='col-9'),
                html.Output(id="total_tax_discount", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Income Tax Base: ", html_for="income_tax_base", className='col-9'),
                html.Output(id="income_tax_base", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Income Tax: ", html_for="income_tax", className='col-9'),
                html.Output(id="income_tax", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Min Wage Discount: ", html_for="minimum_wage_discount", className='col-9'),
                html.Output(id="minimum_wage_discount", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Tax to Pay: ", html_for="tax_to_pay", className='col-9'),
                html.Output(id="tax_to_pay", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Stump Tax: ", html_for="stamp_duty", className='col-9'),
                html.Output(id="stamp_duty", className='col-3 text-end')
            ], className="bg-secondary text-white justify-content-between"),
            dbc.Row([
                dbc.Label("Total Legal Cuts: ", html_for="total_legal_cuts", className='col-9'),
                html.Output(id="total_legal_cuts", className='col-3 text-end')
            ], className="justify-content-between"),
            dbc.Row([
                dbc.Label("Net Income: ", html_for="net_income", className='col-9'),
                html.Output(id="net_income", className='col-3 text-end')
            ], className="fw-bold fs-3 bg-secondary text-white justify-content-between mt-auto"),
        ], className="border border-3 border-primary d-flex flex-column"),
    ], className="border border-3 border-primary"),
], style={'padding-top': '30px'}, id="payroll_detail")

payroll_calculation = dbc.Container([
    dcc.Store(id='saved_payment', data=False),
    dbc.Row([
        dbc.Col([
            dbc.Label("Payment Date: ", html_for="payment-date-div"),
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
            dbc.Label("Payment Type:", html_for="payment_type"),
            dcc.Dropdown(
                options={
                    "wage": "Wage",
                    "premium": "Premium",
                    "dividend": "Dividend",
                    "wage_disparity": "Wage Disparity"
                }, value="wage", id="payment_type"
            ),
        ], className='col-2'),
        dbc.Col([
            dbc.Label("Payment Compound:", html_for="payment_compound"),
            dbc.Input(type="number", value=1, min=0, max=100, step=0.01,
                      id="payment_compound"),
        ], id="compound", className='col-2'),
        dbc.Col([
            dbc.Label("Overtime(hour):", html_for="overtime_hour"),
            dbc.Input(type="number", value=0, min=0, max=55, step=1,
                      id="overtime_hour"),
        ], className='col-2', id="overtime_component"),
        dbc.Col([
            dbc.Button('Calculate', id='calculate_payroll', className="btn btn-success"),
        ], className="align-self-end mb-2 col-1"),
        dbc.Col([
            dbc.Button('Save', id='save_payroll', className="btn btn-warning"),
        ], className="align-self-end mb-2 col-1"),
        dbc.Col([
            dbc.Button('Update', id='update_payroll', className="btn btn-primary"),
        ], className="align-self-end mb-2 col-2")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                options=[], placeholder="Choose a saved payment.",
                multi=False, id="saved_payment_picker"
            )
        ], className='col-2'),
        dbc.Col([
            dbc.Button('Get', id='pick_saved_payment_button', color="success")
        ], className="col-1"),
        dbc.Col([
            dbc.Button('Show', id='show_saved_payment_button', color="warning")
        ], className="col-2")
    ], className="d-flex", style={'padding-top': '50px'})
])


payroll_page = dbc.Container([
    payroll_modals,
    dbc.Row([
        payroll_calculation
    ]),
    dbc.Row([
        payroll_details
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

    Input('show_saved_payment_button', 'n_clicks'),
    Input('calculate_payroll', 'n_clicks'),
    State("user-id", "data"),
    State("payment_date", "date"),
    State("payment_type", "value"),
    State("overtime_hour", "value"),
    State("payment_compound", "value"),
    State('saved_payment', 'data'),
    State('saved_payment_picker', 'value')
)
def calculate_payroll(show_saved, calculate, user_id, p_date, p_type, overtime, compound, payment_list, s_date):
    year, month, day = p_date.split('-')
    payment_date = datetime(int(year), int(month), int(day)).date()
    t_dict = {"wage": "Maas", "premium": "Ikramiye", "dividend": "Kontrolluk/Temmettu", "wage_disparity": "Maas Farki"}
    if ctx.triggered_id == "calculate_payroll" and calculate is not None:
        payroll = Wage(user_id, p_type, payment_date, compound, overtime)
        p_dict = payroll.payroll_dict
        # print(payroll.p_df.iloc[0])
        # print("************Calculated***********")
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
    elif ctx.triggered_id == "show_saved_payment_button" and show_saved is not None and s_date is not None:
        pay_dict = pd.DataFrame.from_dict(payment_list)
        p_df = pay_dict[pay_dict["pay_period"] == s_date]
        print(p_df)

        print(p_df.iloc[0]['payroll_type'])
        return None, t_dict[p_df.iloc[0]['payroll_type']], s_date, p_df.iloc[0]["cumulative_tax_base"], \
               p_df.iloc[0]["base_wage"], p_df.iloc[0]["higher_education_compensation"], p_df.iloc[0]["seniority_bonus"], \
               p_df.iloc[0]["language_compensation"], p_df.iloc[0]["overtime"], p_df.iloc[0]["overtime_pay"], \
               p_df.iloc[0]["union_bonus"], p_df.iloc[0]["family_support"], \
               p_df.iloc[0]["gross_wage"], p_df.iloc[0]["gross_wage"], p_df.iloc[0]["ins_pre_turnover"], p_df.iloc[0]["insurance_premium"], \
               p_df.iloc[0]["unemployment_premium"], p_df.iloc[0]["disability_discount"], p_df.iloc[0]["private_insurance"], \
               p_df.iloc[0]["union_discount"], p_df.iloc[0]["total_tax_discount"], p_df.iloc[0]["income_tax_base"], \
               p_df.iloc[0]["income_tax"], \
               p_df.iloc[0]["minimum_wage_discount"], p_df.iloc[0]["tax_to_pay"], p_df.iloc[0]["stamp_duty"], \
               p_df.iloc[0]["total_legal_cuts"], p_df.iloc[0]["net_income"]
    else:
        raise PreventUpdate

@app.callback(
    Output('payroll_modal', 'is_open'),
    Output('title_payroll_modal', 'children'),
    Output('body_payroll_modal', 'children'),
    Input('save_payroll', 'n_clicks'),
    Input('close_payroll_modal', 'n_clicks'),
    State("user-id", "data"),
    State('calculated_payroll_data', 'data'),
)
def save_payroll(save_click, modal_click, user_id, data_dict):
    if ctx.triggered_id == 'close_payroll_modal':
        return False, dash.no_update, dash.no_update

    if data_dict is None:
        raise PreventUpdate
    df = pd.DataFrame(data_dict, index={data_dict['overtime']})  # converting to df
    payroll = Payroll(user_id)
    sql_response = payroll.insert_payroll(df)
    if sql_response:
        modal_shown = True
        modal_title = 'Bilgileriniz kaydedilmistir.'
        modal_text = 'Kullanici bilgileriniz basarili bir sekilde kaydedilmistir/guncellenmistir.'
        return modal_shown, modal_title, modal_text
    else:
        modal_shown = True
        modal_title = 'Bilgileriniz kaydedilememistir!'
        modal_text = 'Bilgileriniz kaydedilememistir. Lütfen bilgileriniz kontrol ederek tekrar deneyiniz.'
        return modal_shown, modal_title, modal_text


@app.callback(
    Output('saved_payment_picker', 'options'),
    Output('saved_payment', 'data'),
    Input('pick_saved_payment_button', 'n_clicks'),
    State("user-id", "data"),
    State('saved_payment', 'data'),
    prevent_initial_call=True
)
def show_saved_payments_dates(show_click, user_id, loaded):
    if show_click is None:
        raise PreventUpdate
    else:
        global saved_payrolls
        if ctx.triggered_id == "pick_saved_payment_button" and not loaded:
            payroll = Payroll(user_id)
            saved_payrolls = payroll.select_all_payroll()
            saved_payrolls = saved_payrolls.sort_values(by="pay_period", ascending=False)
            return saved_payrolls['pay_period'].to_list(), saved_payrolls.to_dict()
        else:
            print("veriler yuklenemedi")
            return None, None


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
