from cnx import myDB
from datetime import datetime, timedelta
import calendar


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