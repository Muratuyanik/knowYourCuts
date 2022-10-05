from my_database.admin_data_entry import AdminDataEntry as Ade
# from datetime import datetime


class DisabilityDiscount:
    def __init__(self, disability_level, date):
        self.year = date.year
        self.disability_level = disability_level

    def get_disability_discount(self):
        discount = Ade().select_disability_discount(self.year)
        if self.disability_level == '1':
            disability_discount = discount[0]
        elif self.disability_level == '2':
            disability_discount = discount[1]
        elif self.disability_level == '3':
            disability_discount = discount[2]
        else:
            disability_discount = 0
        return disability_discount
