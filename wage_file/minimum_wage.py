from datetime import datetime

from admin_data_entry import AdminDataEntry as Ade
from social_security import SocialSecurity
from tax import Tax


def calculate_min_wage_discount(period, min_wage):
    month = period.month
    year = period.year
    print(year, month)
    cumulative_discount_base = 0
    admin = Ade()

    if month == 1:
        for count in range(month, 13):
            sgk = SocialSecurity(min_wage)
            tax_base = sgk.gross_wage - sgk.insurance() - sgk.unemployment()
            min_wage_stump_duty = sgk.gross_wage * 0.00759
            discount = Tax(tax_base, cumulative_discount_base, year).calculated_tax
            cumulative_discount_base += tax_base
            print(discount, cumulative_discount_base)
            admin.insert_min_wage_discount(year, count, discount, cumulative_discount_base, min_wage_stump_duty)
    else:
        cumulative_discount_base = float(admin.select_min_wage_discount(year, (month-1))[1])
        for count in range(month, 13):
            sgk = SocialSecurity(min_wage)
            tax_base = sgk.gross_wage - sgk.insurance() - sgk.unemployment()
            min_wage_stump_duty = sgk.gross_wage * 0.00759
            discount = Tax(tax_base, cumulative_discount_base, year).calculated_tax
            cumulative_discount_base += tax_base
            print(discount, cumulative_discount_base)
            admin.update_min_wage_discount(year, count, discount, cumulative_discount_base, min_wage_stump_duty)


calculate_min_wage_discount(datetime(2022, 7, 1).date(), 6471)
