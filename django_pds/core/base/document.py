from django.utils.timezone import now
from mongoengine import Document, StringField, ListField, DateTimeField

from django_pds.core.querysets import PdsBaseQuerySet


class SimpleBaseDocument(Document):
    ItemId = StringField(required=True, max_length=36, db_field='_id')
    meta = {
        'allow_inheritance': False,
        'abstract': True,
        'strict': True
    }

    def __str__(self):
        return self.ItemId


class BaseDocument(SimpleBaseDocument):
    CreatedBy = StringField(required=False, max_length=36)
    CreateDate = DateTimeField(default=now)

    Language = StringField(required=True, default='en-US')

    LastUpdateDate = DateTimeField(default=now)
    LastUpdateBy = StringField(required=False)

    Tags = ListField(StringField(min_length=3), default=[])

    IdsAllowedToRead = ListField(StringField(max_length=36), default=[])
    IdsAllowedToWrite = ListField(StringField(max_length=36), default=[])
    IdsAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    IdsAllowedToDelete = ListField(StringField(max_length=36), default=[])

    RolesAllowedToRead = ListField(StringField(max_length=36), default=[])
    RolesAllowedToWrite = ListField(StringField(max_length=36), default=[])
    RolesAllowedToUpdate = ListField(StringField(max_length=36), default=[])
    RolesAllowedToDelete = ListField(StringField(max_length=36), default=[])

    meta = {
        'allow_inheritance': False,
        'abstract': True,
        'strict': True,
        'queryset_class': PdsBaseQuerySet
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.CreateDate = now()
        document.LastUpdateDate = now()