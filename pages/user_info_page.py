from datetime import date, datetime
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from app import app
from user_info import UserInfo
from user_information import UsersInfo
from dash_extensions import BeforeAfter

request_modals = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle(id='title_request_modal')),
    dbc.ModalBody(id='body_request_modal'),
    dbc.ModalFooter(dbc.Button("Close", id="close_request_modal")),
],
    id="request_modal",
    is_open=False,
)

user_info_button = dbc.Row([
    dbc.Col([
        dbc.Button('Get User Data / Fill Your Data', id='show_user_info_button',
                   style={'background-color': 'rgb(0, 0, 209)'}, color="success")
    ],
        width={'size': 'auto'})
], style={'padding-bottom': '50px'}, justify='center')

request_form = dbc.Form([
    dbc.Row([
        dbc.Col([
            dbc.Label("User Name", html_for="active_user", style={"font-weight": "bold"}),
            dbc.Input(type="text", disabled=True, id="active_user")
        ], width="4"),
        dbc.Col([
            dbc.Label("Date", html_for="request_submission_date", style={"font-weight": "bold"}),
            dbc.Input(type="date", disabled=True, value=date.today(), id="request_submission_date")
        ], width={"offset": 2, "size": 2})
    ], style={'padding-top': '10px'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Corporate Starting Date: ", html_for="corporate_starting_date",
                      style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='corporate_starting_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Starting Date", )
        ], width="4"),
        dbc.Col([
            dbc.Label("Experience Before This Corporate (as day): ", html_for="experience_before", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, step=1, style={'text-align': 'right'}, id="experience_before"),
        ], width={"offset": 2, "size": 3}),
    ], ),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Title", html_for="job_title", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "Expert": "Expert",
                    "Technical Expert": "Technical Expert",
                    "Management Staff": "Management Staff",
                    "Engineer": "Engineer"
                }, value="Yok", id="job_title"
            )
        ], width="4"),
    ], ),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Last Education Level", html_for="education_level", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "High School": "High School",
                    "Associate": "Associate",
                    "Bachelor": "Bachelor",
                    "Master": "Master/MBA",
                    "PHD": "PHD"
                }, value="Yok", id="education_level"
            )
        ], width="4"),
        dbc.Col([
            dbc.Label("Graduation Date: ", html_for="graduation_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='graduation_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width={'size': 3, "offset": 2}),
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Marital Status", html_for="marriage", style={"font-weight": "bold"}),
            dcc.RadioItems(['Married', 'Single'], 'Single', inline=True, id='marriage',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width="4"),
    ], ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Spouse Working Status", html_for="partner", style={"font-weight": "bold"}),
            dcc.RadioItems(['Not Working', 'Working'], 'Not Working', inline=True, id='partner',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Starting Date: ", html_for="partner_working_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='partner_working_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width={"offset": 2}),
        dbc.Col([
            dbc.Label("End Date: ", html_for="partner_working_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='partner_working_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Indefinite", )
        ], width={"offset": 0})
    ], style={'padding-top': '0px', 'display': 'flex'}, justify='evenly', align='center', id='partner_status'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Number of Child", html_for="dependent_children", style={"font-weight": "bold"}),
            dcc.RadioItems(['None', '1', '2', '3'], 'None', inline=True, id='dependent_children',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width="4"),
    ], ),
    dbc.Row([
        dbc.Col([
            dbc.Label("1. Child Gender", html_for="child_one_gender", style={"font-weight": "bold"}),
            dcc.RadioItems(['Male', 'Female'], 'Female', inline=True, id='child_one_gender',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Birth Date: ", html_for="child_one_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_one_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width=3),
        dbc.Col([
            dbc.Label("Dependent Status", html_for="child_one_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Dependent', 'Not'], 'dependent', inline=True, id='child_one_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Disability Status", html_for="child_one_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='child_one_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_one_status'),
    dbc.Row([
        dbc.Col([
            dbc.Label("2. Child Gender", html_for="child_two_gender", style={"font-weight": "bold"}),
            dcc.RadioItems(['Male', 'Female'], 'Male', inline=True, id='child_two_gender',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Birth Date: ", html_for="child_two_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_two_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width=3),
        dbc.Col([
            dbc.Label("Dependent Status", html_for="child_two_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Dependent', 'Not'], 'Dependent', inline=True, id='child_two_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Disability Status", html_for="child_two_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='child_two_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_two_status'),
    dbc.Row([
        dbc.Col([
            dbc.Label("3. Child Gender", html_for="child_three_gender", style={"font-weight": "bold"}),
            dcc.RadioItems(['Male', 'Female'], 'Female', inline=True, id='child_three_gender',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Birth Date: ", html_for="child_three_birth_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='child_three_birth_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width=3),
        dbc.Col([
            dbc.Label("Dependent Status", html_for="child_three_dependent", style={"font-weight": "bold"}),
            dcc.RadioItems(['Dependent', 'Not'], 'Dependent', inline=True, id='child_three_dependent',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
        dbc.Col([
            dbc.Label("Disability Status", html_for="child_three_disability", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='child_three_disability',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='3'),
    ], style={'padding-top': '30px', 'display': 'flex'}, justify='evenly', align='center', id='child_three_status'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Disability Status", html_for="disability_level", style={"font-weight": "bold"}),
            dcc.Dropdown(
                options={
                    "None": "No Disability",
                    "1": "First Degree(%80+)",
                    "2": "Second Degree(%60-79)",
                    "3": "Third Degree(%40-59)"
                }, value="None", id="disability_level"
            )
        ], width="4"),
        dbc.Col([
            dbc.Label("Start Date: ", html_for="disability_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='disability_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width={"offset": 2}, id='dis_start'),
        dbc.Col([
            dbc.Label("End Date: ", html_for="disability_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='disability_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Indefinite", )
        ], width={"offset": 0}, id='dis_end')
    ], ),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Private Health Ins", html_for="private_insurance", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='private_insurance',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Ins Start Date: ", html_for="insurance_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='insurance_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Ins Start Date",
                date=datetime.now().date(), )
        ], width={"offset": 2}, id='ins_date'),
        dbc.Col([
            dbc.Label("Total Insurance Amount: ", html_for="total_insurance", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, min=0, step=0.01, style={'text-align': 'right'}, id="total_insurance"),
        ], id="total_cost"),
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Union Membership", html_for="union_membership", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='union_membership',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Start Date: ", html_for="union_start_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='union_start_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                clearable=True,
                initial_visible_month=datetime.now().date(),
                date=datetime.now().date(), )
        ], width={"offset": 2}, id='union_start'),
        dbc.Col([
            dbc.Label("End Date: ", html_for="union_end_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='union_end_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Indefinite", )
        ], width={"offset": 0}, id='union_end')
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Foreign Language", html_for="language", style={"font-weight": "bold"}),
            dcc.RadioItems(['Yes', 'No'], 'No', inline=True, id='language',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ], width='4'),
        dbc.Col([
            dbc.Label("Exam Date: ", html_for="exam_date", style={"font-weight": "bold"}),
            dcc.DatePickerSingle(
                id='exam_date',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date(2050, 9, 19),
                initial_visible_month=datetime.now().date(),
                clearable=True,
                placeholder="Exam Date",
                date=datetime.now().date(), )
        ], width={"offset": 2}, id="lang_date"),
        dbc.Col([
            dbc.Label("Score: ", html_for="exam_score", style={"font-weight": "bold"}),
            dbc.Input(type="number", value=0, min=0, max=100, step=0.25, style={'text-align': 'right'},
                      id="exam_score"),
        ], id="lang_score"),
    ]),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Label("Working Place", html_for="request_submission_date", style={"font-weight": "bold"}),
            dcc.RadioItems(['BANK', 'Other'], 'BANK', inline=True, id='corporation',
                           labelStyle={'display': 'block', 'cursor': 'pointer', 'margin-right': '40px'})
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Button('Save/Update', id='submit_request', style={'background-color': 'rgb(0, 150, 09)'})
        ],
            width={'size': 'auto', 'offset': 9})
    ], style={'padding-top': '40px', 'padding-bottom': '40px'})
], style={'display': 'none'}, id='submission_form')

user_info_page = dbc.Container([
    dbc.Row([
        user_info_button
    ]),
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
    State("user-id", "data"),
    State("corporate_starting_date", "date"),
    State("experience_before", "value"),
    State("job_title", "value"),
    State("education_level", "value"),
    State("graduation_date", "date"),
    State("marriage", "value"),
    State("partner", "value"),
    State("partner_working_start_date", "date"),
    State("partner_working_end_date", "date"),
    State("dependent_children", "value"),
    State("child_one_gender", "value"),
    State("child_one_birth_date", "date"),
    State("child_one_dependent", "value"),
    State("child_one_disability", "value"),
    State("child_two_gender", "value"),
    State("child_two_birth_date", "date"),
    State("child_two_dependent", "value"),
    State("child_two_disability", "value"),
    State("child_three_gender", "value"),
    State("child_three_birth_date", "date"),
    State("child_three_dependent", "value"),
    State("child_three_disability", "value"),
    State("disability_level", "value"),
    State("disability_start_date", "date"),
    State("disability_end_date", "date"),
    State("private_insurance", "value"),
    State("insurance_date", "date"),
    State("total_insurance", "value"),
    State("union_membership", "value"),
    State("union_start_date", "date"),
    State("union_end_date", "date"),
    State("language", "value"),
    State("exam_date", "date"),
    State("exam_score", "value"),
    prevent_initial_call=True
)
def insert_user_inf(sub_click, modal_click, user_id, c_start, experience, title, edu_level, gra_date, marriage, partner,
                    p_start, p_end, d_children, gender1, birth_date1, dependent1, disability1, gender2, birth_date2,
                    dependent2, disability2, gender3, birth_date3, dependent3, disability3, disability_level, d_start,
                    d_end, private_ins, ins_date, ins_total, union, u_start, u_end, language, e_date, score):
    if ctx.triggered_id == 'close_request_modal':
        return False, dash.no_update, dash.no_update, dash.no_update

    data_dict = {"education_level": {"graduation_date": gra_date,
                                     "level": edu_level},
                 "corporate_staff": {"title": title,
                                     "start_date": c_start,
                                     "public_service_time": experience},
                 }
    if disability_level != "None":
        data_dict["disability"] = {"start_date": d_start,
                                   "end_date": d_end,
                                   "level": disability_level}
    if marriage == "Married":
        data_dict["partner_working_status"] = {"start_date": p_start,
                                               "end_date": p_end,
                                               "status": partner}
    if d_children != "None":
        if int(d_children) >= 1:
            data_dict["dependent_child"] = {"birth_date": birth_date1,
                                            "gender": gender1,
                                            "status": dependent1,
                                            "disability": disability1}
        if int(d_children) >= 2:
            pass

    print(data_dict)

    if union == "Yes":
        data_dict["labor_union"] = {"start_date": u_start,
                                    "end_date": u_end}

    if private_ins == "Yes":
        data_dict["private_insurance"] = {"insurance_date": ins_date,
                                          "total_insurance_payment": ins_total}
    if language == "Yes":
        data_dict["language"] = {"exam_date": e_date,
                                 "score": score}

    if None in data_dict.values() or '' in data_dict.values() or c_start is None:
        raise PreventUpdate

    user = UserInfo(user_id)
    sql_response = user.set_user_info(data_dict)
    print(data_dict)
    print(sql_response)
    if sql_response:
        modal_shown = True
        modal_title = 'User information is saved.'
        modal_text = 'User information is successfully saved/updated.'
        sub_result = True
        return modal_shown, modal_title, modal_text, sub_result
    else:
        modal_shown = True
        modal_title = 'User information can not be successfully saved!'
        modal_text = 'User information is not saved. Please carefully check your information and try again.'
        sub_result = False
        return modal_shown, modal_title, modal_text, sub_result


@app.callback(
    Output("active_user", "value"),
    Input("login-control-button", "n_clicks"),
    State("username-box", "value")
)
def user_name(log_click, uname):
    if log_click is None:
        raise PreventUpdate
    else:
        return uname


@app.callback(
    Output("submission_form", "style"),
    Output("corporate_starting_date", "date"),
    Output("experience_before", "value"),
    Output("job_title", "value"),
    Output("education_level", "value"),
    Output("graduation_date", "date"),
    Output("marriage", "value"),
    Output("partner", "value"),
    Output("partner_working_start_date", "date"),
    Output("partner_working_end_date", "date"),
    Output("dependent_children", "value"),
    Output("child_one_gender", "value"),
    Output("child_one_birth_date", "date"),
    Output("child_one_dependent", "value"),
    Output("child_one_disability", "value"),
    Output("child_two_gender", "value"),
    Output("child_two_birth_date", "date"),
    Output("child_two_dependent", "value"),
    Output("child_two_disability", "value"),
    Output("child_three_gender", "value"),
    Output("child_three_birth_date", "date"),
    Output("child_three_dependent", "value"),
    Output("child_three_disability", "value"),
    Output("disability_level", "value"),
    Output("disability_start_date", "date"),
    Output("disability_end_date", "date"),
    Output("private_insurance", "value"),
    Output("insurance_date", "date"),
    Output("total_insurance", "value"),
    Output("union_membership", "value"),
    Output("union_start_date", "date"),
    Output("union_end_date", "date"),
    Output("language", "value"),
    Output("exam_date", "date"),
    Output("exam_score", "value"),
    Input("show_user_info_button", "n_clicks"),
    Input("user-id", "data"),
)
def show_user_form(log_click, user_id):
    style = {"border": "1px solid gray", "padding": "10px", 'background-color': 'rgb(160, 216, 230)'}

    if log_click is None:
        raise PreventUpdate
    else:
        user = UsersInfo(user_id)
        user_dict = user.select_user_info()
        if not user_dict['corporate_staff']:
            return style, None, 0, None, None, datetime.now().date(), "Single", None, None, None, "None", None, None, \
                   None, None, None, None, None, None, None, None, None, None, "No", None, None, "No", None, None, \
                   "No", None, None, "No", None, None
        else:
            if not user_dict['partner_working_status']:
                marital_status = "Single"
                working, p_start, p_end = None, None, None
            else:
                marital_status = "Married"
                working = "Working" if user_dict['partner_working_status'][0][4] == "working" else "Not Working"
                p_start = user_dict['partner_working_status'][0][2]
                p_end = user_dict['partner_working_status'][0][3] if user_dict['partner_working_status'][0][3] else None

            gender1, birth1, status1, disability1 = None, None, None, None
            gender2, birth2, status2, disability2 = None, None, None, None
            gender3, birth3, status3, disability3 = None, None, None, None

            if not user_dict['dependent_child']:
                number_of_child = "None"

            else:
                number_of_child = len(user_dict['dependent_child'])
                if number_of_child >= 1:
                    gender1, birth1, status1, disability1 = user_dict['dependent_child'][0][3], \
                                                            user_dict['dependent_child'][0][2], \
                                                            user_dict['dependent_child'][0][4], \
                                                            user_dict['dependent_child'][0][5]
                if number_of_child >= 2:
                    gender2, birth2, status2, disability2 = user_dict['dependent_child'][1][3], \
                                                            user_dict['dependent_child'][1][2], \
                                                            user_dict['dependent_child'][1][4], \
                                                            user_dict['dependent_child'][1][5]
                if number_of_child == 3:
                    gender3, birth3, status3, disability3 = user_dict['dependent_child'][2][3], \
                                                            user_dict['dependent_child'][2][2], \
                                                            user_dict['dependent_child'][2][4], \
                                                            user_dict['dependent_child'][2][5]

            if not user_dict['disability']:
                self_disability = "None"
                d_start, d_end = None, None
            else:
                self_disability = user_dict['disability'][0][4]
                d_start, d_end = user_dict['disability'][0][2], user_dict['disability'][0][3] if \
                    user_dict['disability'][0][3] else None

            if not user_dict['private_insurance']:
                insurance = "No"
                i_start, total_ins = None, None
            else:
                insurance = "Yes"
                i_start, total_ins = user_dict['private_insurance'][0][2], float(user_dict['private_insurance'][0][3])

            if not user_dict['labor_union']:
                union = "No"
                u_start, u_end = None, None
            else:
                union = "Yes"
                u_start, u_end = user_dict['labor_union'][0][2], user_dict['labor_union'][0][3]

            if not user_dict['language']:
                language = "No"
                e_date, e_score = None, None
            else:
                language = "Yes"
                e_date, e_score = user_dict['language'][0][2], float(user_dict['language'][0][3])

            job_title = user.select_user_title()[0]

            return style, user_dict['corporate_staff'][0][3], user_dict['corporate_staff'][0][4], job_title, \
                   user_dict['education_level'][0][3], user_dict['education_level'][0][2], marital_status, working, \
                   p_start, p_end, str(number_of_child), gender1, birth1, status1, disability1, gender2, birth2, \
                   status2, disability2, gender3, birth3, status3, disability3, self_disability, d_start, d_end, \
                   insurance, i_start, total_ins, union, u_start, u_end, language, e_date, e_score


@app.callback(
    Output(component_id='ins_date', component_property='style'),
    Output(component_id='total_cost', component_property='style'),
    [Input(component_id='private_insurance', component_property='value')])
def show_hide_private_insurance(visibility_state):
    if visibility_state == 'Yes':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'No':
        return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='lang_date', component_property='style'),
    Output(component_id='lang_score', component_property='style'),
    [Input(component_id='language', component_property='value')])
def show_hide_language(visibility_state):
    if visibility_state == 'Yes':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'No':
        return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='union_start', component_property='style'),
    Output(component_id='union_end', component_property='style'),
    [Input(component_id='union_membership', component_property='value')])
def show_hide_union(visibility_state):
    if visibility_state == 'Yes':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'No':
        return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='dis_start', component_property='style'),
    Output(component_id='dis_end', component_property='style'),
    [Input(component_id='disability_level', component_property='value')])
def show_hide_disability(visibility_state):
    if visibility_state != 'None':
        return {'display': 'flex', 'flex-direction': 'column'}, {'display': 'flex', 'flex-direction': 'column'}
    if visibility_state == 'None':
        return {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output(component_id='partner_status', component_property='style'),
    [Input(component_id='marriage', component_property='value')])
def show_hide_partner(visibility_state):
    if visibility_state == 'Married':
        return {'display': 'flex'}
    if visibility_state == 'Single':
        return {'display': 'none'}


@app.callback(
    Output(component_id='child_one_status', component_property='style'),
    Output(component_id='child_two_status', component_property='style'),
    Output(component_id='child_three_status', component_property='style'),
    [Input(component_id='dependent_children', component_property='value')])
def show_hide_children(visibility_state):
    if visibility_state == 'None':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    if visibility_state == '1':
        return {'display': 'flex'}, {'display': 'none'}, {'display': 'none'}
    if visibility_state == '2':
        return {'display': 'flex'}, {'display': 'flex'}, {'display': 'none'}
    if visibility_state == '3':
        return {'display': 'flex'}, {'display': 'flex'}, {'display': 'flex'}
