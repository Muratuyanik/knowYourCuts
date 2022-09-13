import calendar
from datetime import timedelta

from kycDBmanager import AdminDataEntry as Ade


class SocialSecurity:
    """
    Gets gross_wage, payment_date, ins_turnover_base, turnover
    :returns insurance_premium, unemployment_premium and insurance_turnover
    """
    def __init__(self, gross_wage, turnover=0):
        self.gross_wage = gross_wage
        self.previous_turnover = turnover

    def insurance(self):
        insurance_premium = self.gross_wage * .14 + self.previous_turnover
        return insurance_premium

    def insurance_turnover(self, payment_date, ins_turnover_base):
        total_ins_base = self.gross_wage + ins_turnover_base
        maks_insurance_base = float(Ade().select_min_wage(payment_date)) * 7.5
        if payment_date.month % 6 == 1:
            days_in_month = calendar.monthrange(payment_date.year, payment_date.month)[1]
            date = payment_date - timedelta(days=days_in_month)
            maks_insurance_base = (float(Ade().select_min_wage(date)) * 7.5 * 16/30) + \
                                  (float(Ade().select_min_wage(payment_date)) * 7.5 * 14/30)

        print('sigorta tavani:', maks_insurance_base)
        print('toplam sigorta matrahi:', total_ins_base)

        insurance_turnover = 0
        if total_ins_base > maks_insurance_base:
            insurance_turnover = total_ins_base - maks_insurance_base
        return insurance_turnover

    def insurance_employer(self):
        insurance_premium_employer = self.gross_wage * .205
        return insurance_premium_employer

    def unemployment(self):
        unemployment_premium = self.gross_wage * .01
        return unemployment_premium

    def unemployment_employer(self):
        unemployment_premium_employer = self.gross_wage * .02
        return unemployment_premium_employer
