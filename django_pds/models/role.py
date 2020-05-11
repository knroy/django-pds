from mongoengine import StringField, ListField, BooleanField

from django_pds.core.base import SimpleBaseDocument


class Role(SimpleBaseDocument):
    RoleName = StringField(required=True)
    ParentRoles = ListField(StringField())
    IsDynamic = BooleanField(default=False)

    meta = {'collection': 'Roles'}
