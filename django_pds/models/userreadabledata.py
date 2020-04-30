from mongoengine import StringField, ListField, Document


class UserReadableData(Document):

    ItemId = StringField(required=True, max_length=36, db_field='_id')
    EntityName = StringField(max_length=120, required=True, null=False)
    UserReadableFields = ListField(StringField(null=False), required=True)

    meta = {'collection': 'UserReadableDatas'}
