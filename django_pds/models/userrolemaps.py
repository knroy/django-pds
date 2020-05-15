from mongoengine import StringField

from django_pds.core.base import BaseDocument


class UserRoleMap(BaseDocument):

    RoleName = StringField(required=True)
    RoleId = StringField(required=False, max_length=36)
    UserId = StringField(required=True, max_length=36)

    meta = {'collection': 'UserRoleMaps'}
