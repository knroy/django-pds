from uuid import uuid4

from .manager import BaseManager

USER_ROLE_MAP = 'UserRoleMap'


class UserRoleMapsManager(BaseManager):

    def get_user_roles(self, user_id):
        return self.get_document(USER_ROLE_MAP).objects(IdsAllowedToRead=user_id).distinct(field='RoleName')

    def create_user_role_map(self, role_name, user_id):
        try:
            role = self.get_document(USER_ROLE_MAP)()
            role.ItemId = str(uuid4())
            role.RoleName = role_name
            role.IdsAllowedToRead = [user_id]
            role.save()
            return False, role.ItemId
        except BaseException as e:
            return True, e
