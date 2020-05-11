from .base import BaseController

USER_READABLE_DATA = "UserReadableData"


class UserReadableDataController(BaseController):

    def __get_filter(self, entity_name, roles, exclude_default):

        if roles:
            if not isinstance(roles, (list, tuple)):
                return True, 'roles must be a list or tuple type'
            if 'default' not in roles:
                if not exclude_default:
                    roles.append('default')
        else:
            roles = []
            if not exclude_default:
                roles = ['default']

        return {
            'EntityName': entity_name,
            'Role__in': roles
        }

    def get_user_readable_data_fields(self, entity_name, roles=None, exclude_default=False):
        _filter = self.__get_filter(entity_name, roles, exclude_default)
        user_readable_data_s = self.get_document(USER_READABLE_DATA).objects(**_filter)
        if user_readable_data_s.count() > 0:
            fields = []
            for urd in user_readable_data_s:
                fields.append(set(urd.UserReadableFields))
            data = set().union(*fields)
            return False, data
        return True, []
