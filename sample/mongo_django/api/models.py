from mongoengine import ListField, StringField, IntField

from django_pds.core.base import BaseDocument, SimpleBaseDocument


class Patient(BaseDocument):
    name = StringField(required=True, max_length=80)
    age = IntField(min_value=0, required=True)
    contact = StringField(required=True, max_length=15)

    meta = {'collection': 'Patients'}


class Page(SimpleBaseDocument):
    title = StringField(max_length=200, required=True)
    tags = ListField(StringField(required=True), required=True)


class BlogPost(BaseDocument):
    Title = StringField(max_length=2000, required=True)
    Categories = ListField(StringField(required=True), required=False, default=[])
    Views = IntField(min_value=0, default=0)
    Likes = IntField(min_value=0, default=0, )
    FeaturedImageUrl = StringField(required=False, default=None)
