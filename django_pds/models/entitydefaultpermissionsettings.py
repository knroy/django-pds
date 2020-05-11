from mongoengine import StringField, ListField

from django_pds.core.base import SimpleBaseDocument


class EntityDefaultPermissionSetting(SimpleBaseDocument):
    EntityName = StringField(required=True)
    IdsAllowedToRead = ListField(StringField(max_length=36), default=[])
    IdsAllowedToWrite = ListField(StringField(max_length=36), default=[])
    IdsAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    IdsAllowedToDelete = ListField(StringField(max_length=36), default=[])
    RolesAllowedToRead = ListField(StringField(max_length=36), default=[])
    RolesAllowedToWrite = ListField(StringField(max_length=36), default=[])
    RolesAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    RolesAllowedToDelete = ListField(StringField(max_length=36), default=[])

    meta = {'collection': 'EntityDefaultPermissionSettings'}
