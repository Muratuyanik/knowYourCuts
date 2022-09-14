from datetime import datetime, timedelta
from get_user_info import UserInfo

corporate = True
my_dict = {}

# my_dict["disability"] = {
#     "start_date": '2021-09-21',
#     "end_date": None,
#     "level": 3
# }
my_dict["partner_working_status"] = {
    "start_date": '2015-06-01',
    "end_date": None,
    "status": 'not_working'
}
my_dict["private_insurance"] = {
    "insurance_date": '2021-03-25',
    "total_insurance_payment": 4289.04,
}
my_dict["language"] = {
    "exam_date": '2015-09-21',
    "score": 68.75
}
my_dict["education_level"] = {
    "graduation_date": '2011-06-24',
    "level": "Bachelor"
}
my_dict["ilbank_staff"] = {
    "title": 'Uzman',
    "start_date": '2014-01-07',
    "public_service_time": 1000
}
my_dict["labor_union"] = {
    "start_date": '2019-11-24',
    "end_date": '2022-08-20'
}
my_dict["dependent_child"] = {
    "birth_date": "2020-08-02",
    "gender": "female",
    "status": "dependent",
    "disability": "no"
}


my_user_id = 2
active_user = UserInfo(my_user_id, datetime(2022, 8, 15).date())

# active_user.set_user_info(True, my_dict)
# active_user.update_user_info(True, my_dict)
# user_dict = active_user.get_user_info()
# print(user_dict)
# active_user.payroll_user_info()
# print(active_user.payroll_user_dict)

# payroll = Wage(my_user_id, user_dict, '2022-08-15')
# print(payroll.gross_wage)
