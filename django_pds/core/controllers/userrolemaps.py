from uuid import uuid4

from .base import BaseController

USER_ROLE_MAP = 'UserRoleMap'


class UserRoleMapsController(BaseController):

    def get_roles(self, user_id):
        roles = self.get_document(USER_ROLE_MAP).objects(UserId=user_id)
        return roles

    def get_user_non_dynamic_roles(self, available_not_dynamic_roles, user_id):
        user_roles = self.get_user_roles(user_id)
        user_roles = set(user_roles)
        available_not_dynamic_roles = set(available_not_dynamic_roles)
        return user_roles.intersection(available_not_dynamic_roles)

    def get_user_roles(self, user_id):
        return self.get_document(USER_ROLE_MAP).objects(UserId=user_id).distinct(field='RoleName')

    def create_user_role_map(self, role_name, user_id):

        try:

            UserRoleMap = self.get_document(USER_ROLE_MAP)

            role = UserRoleMap()
            role.ItemId = str(uuid4())
            role.UserId = user_id
            role.RoleName = role_name

            role.CreatedBy = "system"
            role.LastUpdateBy = "system"

            role.IdsAllowedToRead = [user_id]
            role.IdsAllowedToUpdate = [user_id]
            role.IdsAllowedToWrite = [user_id]

            role.save()

            return False, role.ItemId

        except BaseException as e:
            return True, e
