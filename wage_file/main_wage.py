import calendar
from datetime import datetime, timedelta

import pandas as pd

from admin_data_entry import AdminDataEntry as Ade
from disability_discount import DisabilityDiscount
from payroll import Payroll
from social_security import SocialSecurity
from tax import Tax
from wage_file.gross_wage import GrossWage
from user_info import UserInfo

'''
this class needed?
class WageDisparity:
    """
    only for disparity calculations. (disparity occurs when an increase of wage in first and seventh months)
    Uses wage class to calculate wage and premium disparities.
    """
    def __init__(self, user_id, payment_date, overtime=0, cumulative_tax_base=0):
        self.user_id = user_id
        self.payment_date = payment_date

    def calculate_disparity(self):
        pass

    def calculate_wage_disparity(self):
        wage_disparity = Wage(1, 'wage_disparity', datetime(2022, 9, 15).date())
        print(wage_disparity)

    def calculate_premium_disparity(self):
        premium_disparity = Wage(1, 'wage_disparity', datetime(2022, 9, 15).date())
        print(premium_disparity)
'''


class Wage:
    """
    WageCalculation class.
    Takes user_id, payment_type, payment_date, overtime, cumulative_tax_base as inputs
    Returns payroll dictionary with all details (keys: name of columns, values: float values of these keys)
    Calculates first base to gross wage, then social security cuts and tax discounts, then tax and tax to pay,
    finally gives net income & and all details of wage payroll.
    Calculates only one payment at a time.
    """
    def __init__(self, user_id, payment_type, payment_date, wage_compound, overtime=0, cumulative_tax_base=0):
        self.user_id = user_id
        self.payment_type = payment_type
        self.payment_date = payment_date
        self.wage_compound = wage_compound
        self.month = self.payment_date.month
        self.year = self.payment_date.year
        self.overtime = overtime
        self.cumulative_tax_base = self.calculate_cumulative_tax_base(cumulative_tax_base)
        self.user_info_dict = self.get_user_info(self.payment_date)
        self.payroll_dict = {}
        self.gross_wage = self.calculate_gross_wage()
        self.wage_calculation()

    # getuser info classinda duzenle
    def get_user_info(self, date):
        active_user = UserInfo(self.user_id, date)
        active_user.payroll_user_info()
        user_dict = active_user.payroll_user_dict
        return user_dict

    def wage_calculation(self):
        self.payroll_dict["payment_type"] = self.payment_type
        self.payroll_dict["pay_period"] = self.payment_date
        self.insurance()
        if self.payment_type == 'wage':  # these discounts&bonus only takes place in 'wage' not other types of payments
            self.union_due()
            self.disability_discount()
            self.private_insurance()
            self.minimum_wage_discount()
            self.family_support()
        else:
            for key in ['disability_discount', 'union_bonus', 'union_discount', 'private_insurance',
                        'minimum_wage_discount', 'family_support']:
                self.payroll_dict[key] = 0
            if self.payment_type == 'wage_disparity':
                self.family_support()
        self.tax_discount()
        self.tax_base()
        self.tax()
        self.stamp_duty()
        self.net_income()

    def overtime_payment(self):
        self.payroll_dict['overtime'] = self.overtime
        overtime_base = self.previous_gross_wage()
        overtime_payment = (self.overtime * overtime_base) / 120
        print(overtime_payment)
        self.payroll_dict['overtime_pay'] = round(overtime_payment, 2)
        return overtime_payment

    def previous_gross_wage(self):
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        date = self.payment_date - timedelta(days=days_in_month)
        pre_month_user_info_dict = self.get_user_info(date)  # gets whole dictionary/ is this needed?
        print(pre_month_user_info_dict)
        previous_gross_wage = GrossWage(
            pre_month_user_info_dict['staff_id'], date, self.payment_type,
            pre_month_user_info_dict['education_level'], pre_month_user_info_dict['seniority'],
            pre_month_user_info_dict['language'] if 'language' in pre_month_user_info_dict.keys() else 0).gross_wage
        return previous_gross_wage

    def calculate_gross_wage(self):
        if self.user_info_dict['staff_id']:
            gross_wage = self.corporation_gross_wage()
        else:
            # for other than corporate users
            # this part not written or tested properly right now
            gross_wage = self.user_info_dict['general_user']
            self.payroll_dict['gross_wage'] = round(gross_wage, 2)
            self.payroll_dict['base_wage'] = round(self.user_info_dict['base'], 2)
        return gross_wage

    def corporation_gross_wage(self):
        gross = GrossWage(
            self.user_info_dict['staff_id'], self.payment_date, self.payment_type,
            self.user_info_dict['education_level'], self.user_info_dict['seniority'],
            self.user_info_dict['language'] if 'language' in self.user_info_dict.keys() else 0,
            self.wage_compound)

        gross_wage = gross.gross_wage
        if self.payment_type == 'wage':    # if not overtime & overtime payment will be none!
            gross_wage += self.overtime_payment()
        else:
            self.payroll_dict['overtime_pay'] = 0
            self.payroll_dict['overtime'] = self.overtime
        self.payroll_dict['base_wage'] = gross.base
        self.payroll_dict['gross_wage'] = round(gross_wage, 2)
        self.payroll_dict['higher_education_compensation'] = round(gross.high_edu_compensation, 2)
        self.payroll_dict['seniority_bonus'] = round(gross.year_of_work_bonus, 2)
        self.payroll_dict['language_compensation'] = round(gross.language_compensation, 2)
        return gross_wage

    def general_user_gross_wage(self):
        pass

    def family_support(self):
        family_support = 0
        compound = Ade().select_family_support_compound(self.payment_date)[2]
        print("compound: ", compound)
        if self.payment_type == 'wage_disparity':
            # only pays difference of the two months compounds
            days_in_month = calendar.monthrange(self.year, self.month)[1]
            date = self.payment_date - timedelta(days=days_in_month)
            compound = float(compound - Ade().select_family_support_compound(date)[2]) * (14/30)

        if 'partner_working_status' in self.user_info_dict.keys():
            if self.user_info_dict['partner_working_status'] == 'not_working':
                partner_support = float(compound) * 2273
                family_support += partner_support
        if 'dependent_child_compound' in self.user_info_dict.keys():
            child_support = float(compound) * self.user_info_dict['dependent_child_compound'] * 250
            family_support += child_support

        self.payroll_dict['family_support'] = round(family_support, 2)

    def insurance(self):
        insurance_turnover = Payroll(self.user_id).select_insurance_turnover(self.payment_date)
        print(insurance_turnover)

        ins_base_list = Payroll(self.user_id).select_insurance_base(self.payment_date)
        print(ins_base_list)
        ins_turnover_base = 0
        if ins_base_list:
            for ins in ins_base_list:
                ins_turnover_base += float(ins[0])

        if insurance_turnover:
            sgk = SocialSecurity(self.gross_wage, float(insurance_turnover))
            self.payroll_dict['insurance_balance'] = float(insurance_turnover)
        else:
            sgk = SocialSecurity(self.gross_wage)
            self.payroll_dict['insurance_balance'] = 0
        self.payroll_dict['insurance_premium'] = round(sgk.insurance(), 2)
        self.payroll_dict['unemployment_premium'] = round(sgk.unemployment(), 2)
        self.payroll_dict['ins_pre_turnover'] = sgk.insurance_turnover(self.payment_date, ins_turnover_base)

    def stamp_duty(self):
        stamp_tax = (self.gross_wage + self.payroll_dict['union_bonus']) * .00759
        if self.payment_type == 'wage':
            stamp_tax -= float(Ade().select_min_wage_discount(self.year, self.month)[2])
        self.payroll_dict['stamp_duty'] = round(stamp_tax, 2)

    def private_insurance(self):
        private_insurance = 0
        if 'private_insurance' in self.user_info_dict.keys():
            private_insurance = self.user_info_dict['private_insurance']
        self.payroll_dict['private_insurance'] = round(private_insurance, 2)

    def union_due(self):
        union_discount = 0
        union_bonus = 0
        if 'labor_union' in self.user_info_dict.keys():
            union_due = self.gross_wage / 200
            union_discount = union_due
            if self.month % 3 == 1:
                union_bonus = self.labor_agreement()
        self.payroll_dict['union_bonus'] = union_bonus
        self.payroll_dict['union_discount'] = union_discount

    def labor_agreement(self):
        union_bonus = Ade().select_labor_agreement(self.payment_date)[2]
        return float(union_bonus)

    def disability_discount(self):
        disability_discount = 0
        if 'disability' in self.user_info_dict.keys():
            disability_discount = DisabilityDiscount(self.user_info_dict['disability'],
                                                     self.payment_date).get_disability_discount()
        self.payroll_dict['disability_discount'] = round(disability_discount, 2)

    def tax_discount(self):

        tax_discount = self.payroll_dict['insurance_premium'] + self.payroll_dict['unemployment_premium'] + \
                       self.payroll_dict['disability_discount'] + self.payroll_dict['union_discount'] + \
                       self.payroll_dict['private_insurance']
        self.payroll_dict['total_tax_discount'] = round(tax_discount, 2)

    def tax_base(self):
        tax_base = self.gross_wage - self.payroll_dict['total_tax_discount']
        self.payroll_dict['income_tax_base'] = round(tax_base, 2)

    def calculate_cumulative_tax_base(self, cumulative):
        previous_cumulative = Payroll(self.user_id).select_cumulative_tax_base(self.payment_date)
        if cumulative != 0 or previous_cumulative is None or previous_cumulative[0].year != self.payment_date.year:
            cumulative_tax_base = cumulative
        else:
            cumulative_tax_base = float(previous_cumulative[1])
        return cumulative_tax_base

    def tax(self):
        tax_object = Tax(self.payroll_dict['income_tax_base'], self.cumulative_tax_base, self.year)
        self.payroll_dict['cumulative_tax_base'] = round(tax_object.cumulative_tax_base, 2)
        self.payroll_dict['income_tax'] = round(tax_object.calculated_tax, 2)
        self.payroll_dict['tax_to_pay'] = round(self.payroll_dict['income_tax'] - self.payroll_dict['minimum_wage_discount'], 2)

    def minimum_wage_discount(self):
        min_wage_discount = float(Ade().select_min_wage_discount(self.year, self.month)[0])
        self.payroll_dict['minimum_wage_discount'] = round(min_wage_discount, 2)

    def net_income(self):
        total_legal_cuts = self.payroll_dict['insurance_premium'] + self.payroll_dict['unemployment_premium'] \
                           + self.payroll_dict['tax_to_pay'] + self.payroll_dict['stamp_duty']
        self.payroll_dict['total_legal_cuts'] = round(total_legal_cuts, 2)
        net_income = self.payroll_dict['gross_wage'] - total_legal_cuts + self.payroll_dict['family_support']\
                     + self.payroll_dict['union_bonus']
        self.payroll_dict['net_income'] = round(net_income, 2)


# payroll = Wage(2, 'premium', datetime(2022, 8, 15).date(), cumulative_tax_base=164216)

# print(payroll.user_info_dict)
# print(payroll.payroll_dict)
# print('*'*100 + '\n' + '*'*100)

# payroll2 = Wage(1, 'wage_disparity', datetime(2022, 7, 5).date(), cumulative_tax_base=120000)
# print(payroll2.user_info_dict)
# print(payroll2.payroll_dict)

# payroll2 = Wage(1, 'wage', datetime(2022, 9, 15).date(),1)
# print(payroll2.user_info_dict)
# print(payroll2.payroll_dict)
# df = pd.DataFrame(payroll2.payroll_dict, index={payroll2.payroll_dict['payment_type']})
# print(df)

# payroll3 = Wage(3, 'wage', datetime(2022, 1, 15).date(), overtime=10)
# print(payroll3.user_info_dict)
# print(payroll3.payroll_dict)
