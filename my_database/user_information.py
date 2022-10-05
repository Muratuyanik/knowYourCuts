import pandas as pd
from cnx import myDB
from datetime import datetime, timedelta
import calendar


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






# !!!!!!!!!!!  TRY USER INFO CLASS UPDATE   !!!!!!!!!!!!
