import pandas as pd
from cnx import myDB
from datetime import datetime, timedelta
import calendar


class Users:
    """
    Python Class for connection with MySQL via knowYourCutDB
    to insert new registration or checking user information in the sign-in process
    or updating username and password.
    """

    def __init__(self):
        self.myDB = myDB

    def register(self, name, password, mail):
        user_id = self.myDB.insert(
            'users', user_name=name, user_password=password, email=mail)
        return user_id
    # End of register

    def sign_in(self, username, password):
        condition = 'user_name = %s AND user_password = %s'
        authorization = self.myDB.select(
            'users', condition, 'authorization', 'userID', user_name=username, user_password=password)
        return authorization if authorization else None
    # End of Signin

    def update_user(self, name, password, new_name, new_password):
        condition = 'user_name = %s AND user_password = %s'
        user_id = self.myDB.update(
            'users', condition, name, password, user_name=new_name, user_password=new_password)
        return user_id


class UsersInfo:
    """
        Python Class for connection with MySQL via knowYourCutDB
        to insert/update/delete user personal information needed for calculating wage
        and select queries used while calculating wage.
        """
    # if user doesn't have any information call insert, else call update
    def __init__(self, user_id):
        self.myDB = myDB
        self.user_id = user_id

    # !!!!!!!!  decide all insert & update in different functions or not!

    def insert_general_user(self, gen_dict):
        general_user_id = self.myDB.insert(
            'disability', user_id=self.user_id, gross_wage=gen_dict['gross_wage'],
            period=gen_dict['period'])
        return general_user_id

    def insert_disability(self, disability_dict):
        disability_id = self.myDB.insert(
            'disability', user_id=self.user_id, start_date=disability_dict['start_date'],
            end_date=disability_dict['end_date'], level=disability_dict['level'])
        return disability_id

    def insert_partner_working_status(self, partner_dict):
        partner_id = self.myDB.insert(
            'partner_working_status', user_id=self.user_id, start_date=partner_dict['start_date'],
            end_date=partner_dict['end_date'], status=partner_dict['status'])
        return partner_id

    def insert_dependent_child(self, child_dict):
        child_id = self.myDB.insert(
            'dependent_child', user_id=self.user_id, birth_date=child_dict['birth_date'], gender=child_dict['gender'],
            status=child_dict['status'], disability=child_dict['disability'])
        return child_id

    def insert_private_insurance(self, ins_dict):
        ins_id = self.myDB.insert(
            'private_insurance', user_id=self.user_id, insurance_date=ins_dict['insurance_date'],
            total_ins_payment=ins_dict['total_insurance_payment'])
        return ins_id

    def insert_language(self, lang_dict):
        language_id = self.myDB.insert(
            'language', user_id=self.user_id, exam_date=lang_dict['exam_date'],
            score=lang_dict['score'])
        return language_id

    def insert_education_level(self, edu_dict):
        education_id = self.myDB.insert(
            'education_level', user_id=self.user_id, graduation_date=edu_dict['graduation_date'],
            education_level=edu_dict['level'])
        return education_id

    def insert_labor_union(self, union_dict):
        union_id = self.myDB.insert(
            'labor_union', user_id=self.user_id, start_date=union_dict['start_date'],
            end_date=union_dict['end_date'])
        return union_id

    def insert_corporate_staff(self, corporate_dict):
        condition = 'job_title=%s'
        title_id = self.myDB.select(
            'job_title', condition, 'title_id', job_title=corporate_dict['title'])

        staff_id = self.myDB.insert(
            'corporate_staff', user_id=self.user_id, title_id=title_id, start_date=corporate_dict['start_date'],
            public_service_time=corporate_dict['public_service_time'])
        return staff_id

    def select_user_info(self):
        user_dictionary = {}
        table_list = ['dependent_child', 'disability', 'education_level', 'general_user', 'corporate_staff',
                      'labor_union', 'language', 'partner_working_status', 'private_insurance']

        for table in table_list:
            sql_query = 'SELECT * FROM ' + table + ' WHERE user_id=%s'
            user_dictionary[table] = self.myDB.select_advanced(sql_query, ('user_id', self.user_id))
        return user_dictionary

    def update_disability(self, disability_id, disability_dict):
        condition = 'disability_id = %s'
        self.myDB.update(
            'disability', condition, disability_id, start_date=disability_dict['start_date'],
            end_date=disability_dict['end_date'], level=disability_dict['level'])

    def update_partner_working_status(self, partner_id, partner_dict):
        condition = 'partner_id = %s'
        self.myDB.update(
            'partner_working_status', condition, partner_id, start_date=partner_dict['start_date'],
            end_date=partner_dict['end_date'], status=partner_dict['status'])

    def update_dependent_child(self, child_id, child_dict):
        condition = 'child_id = %s'
        self.myDB.insert(
            'dependent_child', condition, child_id, birth_date=child_dict['birth_date'],  gender=child_dict['gender'],
            status=child_dict['status'], disability=child_dict['disability'])

    def update_private_insurance(self, insurance_id, ins_dict):
        condition = 'insurance_id = %s'
        self.myDB.update(
            'private_insurance', condition, insurance_id, insurance_date=ins_dict['insurance_date'],
            total_ins_payment=ins_dict['total_insurance_payment'])

    def update_language(self, language_id, lang_dict):
        condition = 'language_id = %s'
        self.myDB.update(
            'language', condition, language_id, exam_date=lang_dict['exam_date'],
            score=lang_dict['score'])

    def update_education_level(self, education_id, edu_dict):
        condition = 'education_id = %s'
        self.myDB.update(
            'education_level', condition, education_id, graduation_date=edu_dict['graduation_date'],
            education_level=edu_dict['level'])

    def update_labor_union(self, labor_union_id, union_dict):
        condition = 'labor_union_id = %s'
        self.myDB.update(
            'labor_union', condition, labor_union_id, start_date=union_dict['start_date'],
            end_date=union_dict['end_date'])

    def update_corporate_staff(self, staff_id, corporate_dict):
        condition = 'title_id=%s'
        title_id = self.myDB.select(
            'job_title', condition, 'title_id', job_title=corporate_dict['title'])

        condition = 'staff_id=%s'
        self.myDB.update(
            'corporate_staff', condition, staff_id, title_id=title_id, start_date=corporate_dict['start_date'],
            public_service_time=corporate_dict['public_service_time'])

# End of Users Class


class AdminDataEntry:
    """
        Python Class for connection with MySQL via knowYourCutDB
        to insert/update/delete wage related base information by admin
        and select queries used while calculating wage.
    """
    def __init__(self):
        self.myDB = myDB

    # Tax Bracket data
    def insert_tax_brackets(self, year, tax_list):
        first, second, third, last = tax_list
        tax_id = self.myDB.insert(
            'tax_brackets', period=year, first=first, second=second, third=third, last=last)
        return tax_id

    def update_tax_brackets(self, year, tax_list):
        first, second, third, last = tax_list
        condition = 'period = %s'
        tax_row_changed = self.myDB.update(
            'tax_brackets', condition, year, first=first, second=second, third=third, last=last)
        return tax_row_changed

    def select_tax_brackets(self, year):
        condition = 'period = %s'
        tax_brackets = self.myDB.select(
            'tax_brackets', condition, 'first', 'second', 'third', 'last', period=year)
        return tax_brackets[0] if tax_brackets else None

    # min wage data
    def insert_min_wage(self, date, wage):
        wage_id = self.myDB.insert(
            'minimum_wage', period=date, gross_wage=wage)
        return wage_id

    def update_min_wage(self, date, wage, new_date, new_wage):
        condition = 'period = %s AND gross_wage = %s'
        changed = self.myDB.update(
            'minimum_wage', condition, date, wage, period=new_date, gross_wage=new_wage)
        return changed

    def select_min_wage(self, date):
        sql_query = 'SELECT gross_wage FROM minimum_wage WHERE period <= %s ' \
                    'ORDER BY period DESC LIMIT 1'
        min_wage = self.myDB.select_advanced(sql_query, ('period', date))
        return min_wage[0] if min_wage else None

    def insert_min_wage_discount(self, year, month, discount, cumulative_discount_base, min_wage_stump_duty):
        tax_discount_id = self.myDB.insert(
            'minimum_wage_tax_discount', year=year, month=month, discount=discount,
            cumulative_discount_base=cumulative_discount_base, min_wage_stump_duty=min_wage_stump_duty)
        return tax_discount_id

    def update_min_wage_discount(self, year, month, discount, cumulative_discount_base, min_wage_stump_duty):
        condition = 'year = %s AND month = %s'
        changed = self.myDB.update(
            'minimum_wage_tax_discount', condition, year, month, discount=discount,
            cumulative_discount_base=cumulative_discount_base, min_wage_stump_duty=min_wage_stump_duty)
        return changed

    def select_min_wage_discount(self, year, month):
        condition = 'year = %s AND month = %s'
        min_tax_discount = self.myDB.select(
            'minimum_wage_tax_discount', condition, 'discount', 'cumulative_discount_base', 'min_wage_stump_duty',
            year=year, month=month)
        return min_tax_discount[0] if min_tax_discount else None

    # to insert or update labor agreement bonus data by admin
    def insert_labor_agreement(self, date, union_bonus):
        labor_id = self.myDB.insert(
            'labor_agreement', period=date, union_bonus=union_bonus)
        return labor_id

    def update_labor_agreement(self, date, union_bonus, new_date, new_union_bonus):
        condition = 'period = %s AND union_bonus = %s'
        changed = self.myDB.update(
            'labor_agreement', condition, date, union_bonus, period=new_date, union_bonus=new_union_bonus)
        return changed

    def select_labor_agreement(self, date):
        sql_query = 'SELECT * FROM labor_agreement WHERE period <= %s ' \
                    'ORDER BY period DESC LIMIT 1'
        union_bonus = self.myDB.select_advanced(sql_query, ('period', date))
        return union_bonus[0] if union_bonus else None

    #  to insert or update corporate staff titles data by admin
    def insert_staff_title(self, title):
        self.myDB.insert(
            'job_title', job_title=title)

    def update_staff_title(self, title, new_title):
        condition = 'job_title = %s'
        changed = self.myDB.update(
            'job_title', condition, title, job_title=new_title)
        return changed

    def select_staff_title(self, title):
        condition = 'job_title = %s'
        title_id = self.myDB.select(
            'job_title', condition, 'title_id', job_title=title)
        return title_id

    # base wage for the corporate workers by position
    def insert_corporate_wage(self, title, wage, period):
        title_id = self.select_staff_title(title)
        ibw_id = self.myDB.insert(
            'corporate_base_wage', title_id=title_id, base_wage=wage, base_period=period)
        return ibw_id

    def update_corporate_wage(self, wage, period, new_wage, new_period):
        condition = 'base_wage=%s AND base_period= %s'
        changed = self.myDB.update(
            'corporate_base_wage', condition, wage, period, base_wage=new_wage, base_period=new_period)
        return changed

    def select_corporate_wage(self, title_id, period):
        sql_query = 'SELECT * FROM corporate_base_wage WHERE title_id=%s AND base_period <= %s ' \
                    'ORDER BY base_period DESC LIMIT 1'
        wage = self.myDB.select_advanced(sql_query, ('title_id', title_id), ('base_period', period))
        return wage[0] if wage else None

    # wage_raise for the corporate workers by position
    def insert_wage_raise(self, wage_raise, raise_date):
        raise_id = self.myDB.insert(
            'wage_raise', wage_raise=wage_raise, raise_date=raise_date)
        return raise_id

    def update_wage_raise(self, wage_raise, raise_date, new_wage_raise, new_raise_date):
        condition = 'base_wage=%s AND base_period= %s'
        changed = self.myDB.update(
            'wage_raise', condition, wage_raise, raise_date, wage_raise=new_wage_raise, base_period=new_raise_date)
        return changed

    def select_wage_raise(self, raise_date):
        sql_query = 'SELECT * FROM wage_raise WHERE raise_date <= %s ORDER BY raise_date DESC LIMIT 1'
        wage_raise = self.myDB.select_advanced(sql_query, ('base_period', raise_date))
        return wage_raise[0] if wage_raise else None

    # amounts of disability discount for yearly
    def insert_disability_discount(self, year, disability_list):
        first, second, third = disability_list
        disability_discount_id = self.myDB.insert(
            'disability_discount', period=year, first=first, second=second, third=third)
        return disability_discount_id

    def update_disability_discount(self, year, disability_list):
        first, second, third = disability_list
        condition = 'period = %s'
        row_changed = self.myDB.update(
            'disability_discount', condition, year, first=first, second=second, third=third)
        return row_changed

    def select_disability_discount(self, year):
        condition = 'period = %s'
        disability_discount = self.myDB.select(
            'disability_discount', condition, 'first', 'second', 'third', period=year)
        return disability_discount[0] if disability_discount else None

    def insert_family_support_compound(self, period, compound):
        compound_id = self.myDB.insert(
            'family_support', period=period, compound=compound)
        return compound_id

    def update_family_support_compound(self, period, compound, new_period, new_compound):
        condition = 'period = %s'
        changed = self.myDB.update('family_support', condition, period, compound, period=new_period,
                                   compound=new_compound)
        return changed

    def select_family_support_compound(self, date):
        sql_query = 'SELECT * FROM family_support WHERE period <= %s ' \
                    'ORDER BY period DESC LIMIT 1'
        compound = self.myDB.select_advanced(sql_query, ('period', date))
        return compound[0] if compound else None


class Payroll:
    def __init__(self, user_id):
        self.myDB = myDB
        self.user_id = user_id

    def insert_payroll(self, payroll_df):
        payroll_df.insert(0, 'user_id', self.user_id)
        payroll_id = self.myDB.insert_advanced('payroll', payroll_df)
        return payroll_id

    def update_payroll(self):
        pass

    def select_payroll(self):
        pass

    def delete_payroll(self):
        pass

    def select_insurance_turnover(self, period):
        days_in_month = calendar.monthrange(period.year, period.month)[1]
        control_date = period - timedelta(days=days_in_month)
        print('control_date:', control_date)
        sql_query = 'SELECT ins_pre_turnover FROM payroll WHERE user_id=%s AND pay_period <= %s AND ' \
                    'pay_period > %s ORDER BY pay_period DESC'
        insurance_turnover = self.myDB.select_advanced(sql_query, ('user_id', self.user_id), ('pay_period', period),
                                                       ('control_date', control_date))
        return insurance_turnover[0] if insurance_turnover else None

    def select_insurance_base(self, period):
        days_in_month = calendar.monthrange(period.year, period.month)[1]
        control_date = period - timedelta(days=days_in_month)
        print('control_date:', control_date)
        sql_query = 'SELECT gross_wage, payroll_type FROM payroll WHERE user_id=%s AND pay_period <= %s AND ' \
                    'pay_period > %s ORDER BY pay_period DESC'
        insurance_turnover = self.myDB.select_advanced(sql_query, ('user_id', self.user_id), ('pay_period', period),
                                                       ('control_date', control_date))
        return insurance_turnover if insurance_turnover else None

    def select_cumulative_tax_base(self, period):
        sql_query = 'SELECT pay_period, cumulative_tax_base FROM payroll WHERE user_id=%s AND pay_period < %s ' \
                    'ORDER BY pay_period DESC LIMIT 1'
        cumulative = self.myDB.select_advanced(sql_query, ('user_id', self.user_id), ('pay_period', period))
        return cumulative[0] if cumulative else None


# !!!!!!!!!!!  TRY USER INFO CLASS UPDATE   !!!!!!!!!!!!

# payroll = Payroll(1)
#
# df = pandas.read_csv('wage.csv')
#
# print(df)
# print(payroll.insert_payroll(df))
