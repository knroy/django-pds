from .base import BaseController

USER_READABLE_DATA = "UserReadableData"


class UserReadableDataController(BaseController):

    def get_user_readable_data_fields(self, entity_name):
        user_readable_data_s = self.get_document(USER_READABLE_DATA).objects(EntityName=entity_name)
        if user_readable_data_s.count() > 0:
            urds = user_readable_data_s[0]
            return False, urds.UserReadableFields
        return True, []

    def get_user_readable_data(self, entity_name):
        user_readable_data_s = self.get_document(USER_READABLE_DATA).objects(EntityName=entity_name)
        if user_readable_data_s.count() > 0:
            urds = user_readable_data_s[0]
            return False, urds
        return True, []
