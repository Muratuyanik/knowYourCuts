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
            'users', condition, 'authorization', 'user_id', user_name=username, user_password=password)
        return authorization[0] if authorization else None
    # End of Signin

    def update_user(self, name, password, new_name, new_password):
        condition = 'user_name = %s AND user_password = %s'
        changed = self.myDB.update(
            'users', condition, name, password, user_name=new_name, user_password=new_password)
        return changed

