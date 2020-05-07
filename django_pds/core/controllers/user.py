from uuid import uuid4

import bcrypt

from django_pds.conf import settings
from .base import BaseController

USER = 'User'

PASSWORD_ENCRYPT_KEY = getattr(settings, 'PASSWORD_ENCRYPTION_KEY', None)


class UserController(BaseController):

    def mail_exists(self, email):
        return self.get_document(USER).objects(Email=email).count() > 0

    def phone_exists(self, phone_number):
        return self.get_document(USER).objects(
            PhoneNumber=phone_number).count() > 0 and phone_number != ''

    def user_name_exists(self, user_name):
        return self.get_document(USER).objects(UserName=user_name).count() > 0

    def get_user_by_id(self, user_id, multiple=True):
        if not multiple:
            return self.get_document(USER).objects(ItemId=user_id)[0]
        return self.get_document(USER).objects(ItemId=user_id)

    def get_user_by_email(self, email):
        return self.get_document(USER).objects(Email=email)

    def get_user_by_username(self, username):
        return self.get_document(USER).objects(UserName=username)

    def get_user_by_phone(self, phone):
        return self.get_document(USER).objects(PhoneNumber=phone)

    def delete_user(self, user_id):
        users = self.get_user_by_id(user_id)
        if users.count() > 0:
            user = users[0]
            user.delete()

    def __is_valid_password(self, hashed_from_db, plain_password):
        hashed_from_plain = self.__hash_password(plain_password)
        return hashed_from_db == hashed_from_plain

    def __hash_password(self, password):

        if not PASSWORD_ENCRYPT_KEY:
            raise Exception(
                'Password encryption key not configured, add \'PASSWORD_ENCRYPTION_KEY\' in django_pds settings file')
        hashed_password = bcrypt.kdf(password.encode('utf8'), PASSWORD_ENCRYPT_KEY.encode('utf8'),
                                     desired_key_bytes=36, rounds=60)
        hashed_password = str(hashed_password)
        return hashed_password

    def create_user(self, username, email, phone, password, **kwargs):

        try:

            hashed_password = self.__hash_password(password)

            User = self.get_document(USER)

            user = User(**kwargs)
            user.ItemId = str(uuid4())
            user.CreatedBy = user.ItemId
            user.LastUpdateBy = user.ItemId
            user.PhoneNumber = phone
            user.Email = email
            user.EmailVerified = False
            user.Password = hashed_password
            user.PhoneVerified = False
            user.UserName = username
            user.Active = False
            user.IdsAllowedToRead = [user.ItemId]
            user.IdsAllowedToUpdate = [user.ItemId]
            user.IdsAllowedToWrite = [user.ItemId]
            user.PublicUserId = user.ItemId.replace("-", "")

            user.save()

            return user.ItemId

        except BaseException as e:
            return e

    def __is_valid_user_for_login(self, user, password):

        hashed_pass = user.Password
        is_valid_user = self.__is_valid_password(hashed_pass, password)
        if is_valid_user:
            return False, user
        return True, 'invalid error credentials provided'

    def check_login(self, password, email=None, username=None, phone=None):

        try:

            if email is not None:
                users = self.get_user_by_email(email)
                if users.count() > 0:
                    user = users[0]
                    return self.__is_valid_user_for_login(user, password)
                else:
                    return True, 'user not found'

            if username is not None:
                users = self.get_user_by_username(username)
                if users.count() > 0:
                    user = users[0]
                    return self.__is_valid_user_for_login(user, password)
                else:
                    return True, 'user not found'

            if phone is not None:
                users = self.get_user_by_phone(phone)
                if users.count() > 0:
                    user = users[0]
                    return self.__is_valid_user_for_login(user, password)
                else:
                    return True, 'user not found'

            return True, 'user not found'

        except BaseException as e:
            return True, e

    def read(self):
        return self.get_document(USER).objects
