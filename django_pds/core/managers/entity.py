from django_pds.conf import settings
from django_pds.core.settings import SECURITY_ATTRIBUTES
from django_pds.serializers import GenericSerializerAlpha
from .manager import BaseManager
from .userrolemaps import UserRoleMapsManager

ENTITY_DEFAULT_PERMISSION_SETTINGS = settings.DOCUMENT_ENTITY_DEFAULT_PERMISSION_SETTING
ADMIN = 'admin'


class DefaultPermissionSettingsManager(BaseManager):

    def __has_permission(self, document_name, row, user_id):
        permissions = self.get_document(ENTITY_DEFAULT_PERMISSION_SETTINGS).objects(
            EntityName=document_name)
        if permissions.count() > 0:
            permission = permissions[0]
            user_role_manager = UserRoleMapsManager()
            user_roles = set(user_role_manager.get_user_roles(user_id))
            permitted_roles = set(getattr(permission, row, []))
            permitted_roles.add(ADMIN)
            common_roles = user_roles.intersection(permitted_roles)
            return len(common_roles) > 0
        return False

    def can_insert(self, document_name, user_id):
        return self.__has_permission(document_name, 'RolesAllowedToWrite', user_id)

    def can_delete(self, document_name, user_id):
        return self.__has_permission(document_name, 'RolesAllowedToDelete', user_id)

    def can_read(self, document_name, user_id):
        return self.__has_permission(document_name, 'RolesAllowedToRead', user_id)

    def can_update(self, document_name, user_id):
        return self.__has_permission(document_name, 'RolesAllowedToUpdate', user_id)

    def get_document_name_permissions(self, document_name):
        try:
            permissions = self.get_document(ENTITY_DEFAULT_PERMISSION_SETTINGS).objects(EntityName=document_name)
            if permissions.count() > 0:
                permission = permissions[0]
                json = GenericSerializerAlpha().document(ENTITY_DEFAULT_PERMISSION_SETTINGS).fields(
                    SECURITY_ATTRIBUTES).serialize(permission)
                return False, json.data
            return True, None
        except BaseException as e:
            return True, str(e)
