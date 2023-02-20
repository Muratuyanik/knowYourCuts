import calendar

from my_database.admin_data_entry import AdminDataEntry as Ade
from datetime import date, timedelta
import datetime


class GrossWage:
    """
    Only work for corporate users/ Call for only corporate staff
    take input related to base wage &  related information
    calculate Gross wage and 3 compensation
    """
    def __init__(self, title_id, payment_date, payment_type, higher_education, seniority, language_level, wage_compound=1):
        self.payment_date = payment_date
        self.payment_type = payment_type
        self.wage_compound = wage_compound
        self.base = self.get_base_wage(title_id)
        self.higher_education = higher_education
        self.seniority = seniority
        self.language_level = language_level
        self.high_edu_compensation = self.higher_education_compensation()
        self.year_of_work_bonus = self.work_year_bonus()
        self.language_compensation = self.language_level_compensation()
        self.gross_wage = self.gross_wage_calculate()

    def gross_wage_calculate(self):
        gross_wage = self.base + self.high_edu_compensation + self.year_of_work_bonus + \
            self.language_compensation

        return gross_wage

    def get_base_wage(self, title_id):
        admin = Ade()
        if self.payment_type == 'wage_disparity':
            raise_rate = float(admin.select_wage_raise(self.payment_date)[1])
            days_in_month = calendar.monthrange(self.payment_date.year, self.payment_date.month)[1]
            pre_date = self.payment_date - timedelta(days=days_in_month)
            base_wage = float(admin.select_corporate_wage(title_id, pre_date)[2]) * (44 / 30) * (raise_rate/100)
        else:
            if self.payment_type == 'wage_disparity':
                base_wage = float(admin.select_corporate_wage(title_id, self.payment_date)[2])*self.wage_compound
            else:
                base_wage = float(admin.select_corporate_wage(title_id, self.payment_date)[2])

        if self.payment_type == 'dividend':
            base_wage *= self.wage_compound

        return base_wage

    def higher_education_compensation(self):
        edu_compensation = 0
        if self.higher_education == 'PHD':
            edu_compensation = self.base * .015
        elif self.higher_education == 'Master':
            edu_compensation = self.base * .01
            
        return edu_compensation

    def work_year_bonus(self):
        seniority_bonus = 0
        if self.seniority >= 20:
            seniority_bonus = self.base * .04
        elif self.seniority >= 15:
            seniority_bonus = self.base * .03
        elif self.seniority >= 10:
            seniority_bonus = self.base * .02
        elif self.seniority >= 5:
            seniority_bonus = self.base * .01

        return seniority_bonus

    def language_level_compensation(self):
        language_compensation = 0
        if self.language_level == 3:
            language_compensation = self.base * .015
        elif self.language_level == 2:
            language_compensation = self.base * .01
        elif self.language_level == 1:
            language_compensation = self.base * .005

        return language_compensation
