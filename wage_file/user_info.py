from my_database.user_information import UsersInfo
from datetime import datetime, timedelta


class UserInfo:
    """
    Gets&Sets userinfo via kycDBmanager class
    Takes & Returns user dictionaries
    """
    def __init__(self, user_id, payroll_date=datetime.now().date()):
        self.user_id = user_id
        self.payroll_date = payroll_date
        self.user = UsersInfo(self.user_id)
        self.payroll_user_dict = {}
        self.table_list = ['dependent_child', 'disability', 'education_level', 'general_user', 'corporate_staff',
                           'labor_union', 'language', 'partner_working_status', 'private_insurance']

    def set_user_info(self, user_dict, corporate=True):

        response_list = []
        for table in self.table_list:
            if table in user_dict.keys():
                insert_function = 'insert_' + table
                if corporate & (table in ('dependent_child', 'disability', 'education_level', 'corporate_staff',
                                          'labor_union', 'language', 'partner_working_status', 'private_insurance')):
                    response_id = getattr(self.user, insert_function)(user_dict[table])
                    response_list.append(response_id)
                else:
                    if table in ('dependent_child', 'disability', 'education_level', 'general_user',
                                 'partner_working_status', 'private_insurance'):
                        response_id = getattr(self.user, insert_function)(user_dict[table])
                        response_list.append(response_id)
        return len(response_list)

    def update_user_info(self, corporate, user_dict):

        # handle IDs for tables  !!!!!!!!!!!!!!!
        for table in self.table_list:
            if table in user_dict.keys():
                update_function = 'update_' + table
                if corporate & (table in ('dependent_child', 'disability', 'education_level', 'corporate_staff',
                                          'labor_union', 'language', 'partner_working_status', 'private_insurance')):
                    getattr(self.user, update_function)(user_dict[table])
                elif table in ('dependent_child', 'disability', 'education_level', 'general_user',
                               'partner_working_status', 'private_insurance'):
                    getattr(self.user, update_function)(user_dict[table])

    def get_user_info(self):
        user_dict = self.user.select_user_info()
        return user_dict

    def payroll_user_info(self):
        user_dict = self.get_user_info()
        for key in self.table_list:
            if user_dict[key]:
                getattr(self, key)(user_dict[key])

    def dependent_child(self, child_dict):
        compound = 0
        for child in child_dict:
            if ((self.payroll_date - child[2]).days < 365*6) & (child[4] == 'dependent'):
                if child[5] == 'yes':
                    compound += 3
                else:
                    compound += 2
            elif ((self.payroll_date - child[2]).days < 365*25) & (child[4] == 'dependent'):
                if child[5] == 'yes':
                    compound += 1.5
                else:
                    compound += 1
        print("dependent_child_compound", compound)
        self.payroll_user_dict["dependent_child_compound"] = compound

    def education_level(self, edu_dict):
        if edu_dict[-1][2] < self.payroll_date:
            self.payroll_user_dict['education_level'] = edu_dict[-1][3]
        # modify to check highest education level
        # for education in edu_dict:
        #     if education[2] < self.payroll_date:
        #         if education[3] == 'PHD':
        #             self.payroll_user_dict['education_level'] = education[3]
        #             break
        #         elif education[3] == 'Master':
        #             self.payroll_user_dict['education_level'] = education[3]
        #         else:
        #             self.payroll_user_dict['education_level'] = education[3]
        #         print(self.payroll_user_dict['education_level'])

    def language(self, language_dict):
        score = language_dict[-1][3]
        exam_date = language_dict[-1][2]
        language_level = 0
        if score > 85:
            language_level = 3
        elif score > 70:
            language_level = 2
        elif score >= 60:
            language_level = 1
        if (self.payroll_date - exam_date).days / 365 > 5:
            language_level -= 1
        self.payroll_user_dict['language'] = language_level

    def corporate_staff(self, staff_dict):
        self.payroll_user_dict['staff_id'] = staff_dict[-1][2]
        seniority = ((self.payroll_date - staff_dict[0][3]).days + staff_dict[0][4])/365
        self.payroll_user_dict['seniority'] = seniority

    def labor_union(self, union_dict):
        if (union_dict[-1][2] < self.payroll_date) & (union_dict[-1][3] is None
                                                      or (union_dict[-1][3] > self.payroll_date)):
            self.payroll_user_dict['labor_union'] = 'labor_union_member'

    def partner_working_status(self, partner_dict):
        for partner in partner_dict:
            if (partner[2] < self.payroll_date) & (partner[3] is None
                                                   or (partner[3] > self.payroll_date)):
                self.payroll_user_dict["partner_working_status"] = partner[4]

    def private_insurance(self, ins_dict):
        private_insurance = 0
        for insurance in ins_dict:
            if (insurance[2] < self.payroll_date) & ((self.payroll_date-insurance[2]).days < 365):
                private_insurance = insurance[3]/12
        self.payroll_user_dict["private_insurance"] = float(private_insurance)

    def disability(self, disability_dict):
        for disability in disability_dict:
            if (disability[2] < self.payroll_date) & (disability[3] is None
                                                      or (disability[3] > self.payroll_date)):
                self.payroll_user_dict["disability"] = disability[4]

    def general_user(self, general_dict):
        pass
