import dash
import numpy as np
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from app import app
from main_wage import Wage
from my_database import user_information
from datetime import datetime, date

from payroll import Payroll

df_of_results = pd.DataFrame({})

payroll_graph = dbc.Container([
    dcc.Store(id='current-data'),
    dcc.Store(id='data-loaded', data=False),
    dcc.Download(id="download-dataframe-csv"),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=date(1995, 8, 5),
                        max_date_allowed=date(2035, 9, 19),
                        initial_visible_month=date(2023, 1, 1),
                        start_date=date(2023, 1, 1),
                        end_date=date(2023, 12, 31)
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button('Show', id='show_selected_button', color="success"),
                    dbc.Button('Download', id='download_raw_data_button', color="warning", className="m-3")
                ], className="align-self-center m-1")
            ], className="d-flex"),
        ]),
        dbc.Col([
            dcc.Graph(id='result-pie-graph')
        ])
    ], className="d-flex", style={'padding-top': '50px'}),
    dbc.Row(
        dcc.Graph(id='result-graph')
    ),
    dbc.Row(
        dbc.Table([[], []], bordered=True, hover=True, responsive=True, id='result-table')
    ),

])

payroll_graphs_page = dbc.Container([
    payroll_graph
])


@app.callback(
    Output("result-table", "children"),
    Output('result-graph', 'figure'),
    Output('result-pie-graph', 'figure'),
    Output("current-data", "data"),
    Input("show_selected_button", "n_clicks"),
    State("user-id", "data"),
    State("my-date-picker-range", "start_date"),
    State("my-date-picker-range", "end_date"),
    prevent_initial_call=True
)
def sonuclariGoster(show_click, user_id, s_date, e_date):
    if show_click is None:
        raise PreventUpdate

    global df_of_results

    if ctx.triggered_id == "show_selected_button":
        payroll = Payroll(user_id)
        saved_payrolls = payroll.select_all_payroll()
        saved_payrolls = saved_payrolls.sort_values(by="pay_period", ascending=False)
        if len(saved_payrolls) == 0:
            empty_graph = go.Figure().add_annotation(x=2, y=2, text="No Data to Display",
                                                     font=dict(family="sans serif", size=25, color="crimson"),
                                                     showarrow=False, yshift=10)
            return None, empty_graph, {}, None, None
        else:
            year, month, day = s_date.split('-')
            start_date = datetime(int(year), int(month), int(day)).date()
            year, month, day = e_date.split('-')
            end_date = datetime(int(year), int(month), int(day)).date()
            date_filter = (saved_payrolls['pay_period'] > start_date) & (saved_payrolls['pay_period'] <= end_date)
            df_payrolls = saved_payrolls.loc[date_filter]
            df_payrolls = df_payrolls.drop(['payroll_id', 'user_id'], axis=1)

            # Table
            table_header = [html.Thead(html.Tr([html.Th(column) for column in df_payrolls.columns]))]
            table_body = [html.Tbody([html.Tr([html.Td(data) for data in row])
                                      for index, row in df_payrolls.iterrows()])]
            # Graph
            df_graph = df_payrolls[["pay_period", "gross_wage", "insurance_premium", "unemployment_premium",
                                    "tax_to_pay", "net_income", 'stamp_duty', "payroll_type"]]
            graph = px.line(df_graph, x='pay_period', y='unemployment_premium', markers=True, )
            graph.add_scatter(x=df_graph['pay_period'], y=df_graph['gross_wage'], name="Gross Wage")
            graph.add_scatter(x=df_graph['pay_period'], y=df_graph['insurance_premium'], name="Social Security")
            graph.add_scatter(x=df_graph['pay_period'], y=df_graph['tax_to_pay'], name="Tax")
            graph.add_scatter(x=df_graph['pay_period'], y=df_graph['net_income'], name="Net Income")

            df_pie = df_graph.drop(["pay_period", "gross_wage", "payroll_type"], axis=1)
            df_pie.loc['Totals'] = df_pie.sum()
            df_piechart = df_pie.iloc[[-1]]
            labels = df_piechart.columns.values.tolist()
            for index, row in df_piechart.iterrows():
                values = [row.insurance_premium, row.unemployment_premium, row.tax_to_pay, row.net_income, row.stamp_duty]
            pie_chart = px.pie(
                data_frame=df_piechart,
                values=values,
                names=labels,
                hole=.2,
            )
            # pie_chart.update_traces(hoverinfo='percent', textinfo="value")
            return (table_header + table_body), graph, pie_chart, df_payrolls.to_dict()


@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('download_raw_data_button', 'n_clicks'),
    State('current-data', 'data'),
    prevent_initial_call=True
)
def hamVeri_indir(click, data):
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "Result_{}.csv".format(int(datetime.now().timestamp())))

