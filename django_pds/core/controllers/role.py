from .base import BaseController

ROLE = 'Role'


class RoleController(BaseController):

    def get_non_dynamic_roles(self):
        return self.get_document(ROLE).objects(IsDynamic=False).distinct(field='RoleName')

    def get_roles(self):
        pass

    def is_dynamic_role(self):
        pass

    def create_role(self, role_name, is_dynamic=True):
        pass
