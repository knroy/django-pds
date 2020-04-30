from mongoengine import StringField, Document


class Entity(Document):

    ItemId = StringField(required=True, max_length=36, db_field='_id')
    EntityName = StringField(max_length=120, required=True, null=False)
    PrimaryEntityName = StringField(max_length=120, required=True, null=False)

    meta = {'collection': 'Entities'}
