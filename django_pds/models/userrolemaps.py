from mongoengine import StringField, ListField

from django_pds.core.base import SimpleBaseDocument


class UserRoleMap(SimpleBaseDocument):
    RoleName = StringField(required=True)
    IdsAllowedToRead = ListField(StringField(required=True), default=[])
    meta = {'collection': 'UserRoleMaps'}
