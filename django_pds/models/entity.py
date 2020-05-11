from mongoengine import StringField

from django_pds.core.base import SimpleBaseDocument


class Entity(SimpleBaseDocument):
    EntityName = StringField(max_length=120, required=True, null=False)
    PrimaryEntityName = StringField(max_length=120, required=True, null=False)

    meta = {'collection': 'Entities'}
