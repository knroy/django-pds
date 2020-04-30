from mongoengine import StringField, ListField, Document


class EntityDefaultPermissionSetting(Document):

    ItemId = StringField(required=True, max_length=36, db_field='_id')
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
