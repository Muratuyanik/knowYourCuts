from datetime import datetime
from kycDBmanager import AdminDataEntry as Ade


class Tax:
    """
    Calculate income tax accordingly tax brackets
    :gets tax base, cumulative tax base, year of payment
    :returns income tax and cumulative tax base
    """
    def __init__(self, tax_base, cumulative_tax_base=0, year=datetime.now().year):
        self.tax_base = tax_base
        self.cumulative_tax_base = cumulative_tax_base + tax_base
        self.calculated_tax = self.calculate_tax(year)

    def calculate_tax(self, year):
        tax_brackets = Ade().select_tax_brackets(year)
        first, second, third, last = tax_brackets

        if self.cumulative_tax_base < first:
            calculated_tax = self.tax_base * 0.15
        elif self.cumulative_tax_base < second:
            if (self.cumulative_tax_base - self.tax_base) > first:
                calculated_tax = self.tax_base * 0.20
            else:
                this_bracket_amount = (self.cumulative_tax_base - first)
                calculated_tax = this_bracket_amount * 0.20 + (self.tax_base - this_bracket_amount) * 0.15
        elif self.cumulative_tax_base < third:
            if (self.cumulative_tax_base - self.tax_base) > second:
                calculated_tax = self.tax_base * 0.27
            else:
                this_bracket_amount = (self.cumulative_tax_base - second)
                calculated_tax = this_bracket_amount * 0.27 + (self.tax_base - this_bracket_amount) * 0.20
        elif self.cumulative_tax_base < last:
            if (self.cumulative_tax_base - self.tax_base) > third:
                calculated_tax = self.tax_base * 0.35
            else:
                this_bracket_amount = (self.cumulative_tax_base - third)
                calculated_tax = this_bracket_amount * 0.35 + (self.tax_base - this_bracket_amount) * 0.27
        else:
            if (self.cumulative_tax_base - self.tax_base) > last:
                calculated_tax = self.tax_base * 0.40
            else:
                this_bracket_amount = (self.cumulative_tax_base - last)
                calculated_tax = this_bracket_amount * 0.40 + (self.tax_base - this_bracket_amount) * 0.35
        return calculated_tax
