from cnx import myDB


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


