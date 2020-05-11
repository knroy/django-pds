from mongoengine import StringField, ListField

from django_pds.core.base import SimpleBaseDocument


class UserReadableData(SimpleBaseDocument):
    EntityName = StringField(max_length=120, required=True, null=False)
    Role = StringField(max_length=120, required=False, default='default')
    UserReadableFields = ListField(StringField(null=False), required=True)

    meta = {'collection': 'UserReadableDatas'}
