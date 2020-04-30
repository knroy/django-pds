from django.utils.timezone import now
from mongoengine import StringField, BooleanField, IntField, DateTimeField, ListField, FloatField

from django_pds.core.base import BaseDocument


class User(BaseDocument):
    
    FirstName = StringField(required=False, max_length=60)
    MiddleName = StringField(required=False, max_length=60)
    LastName = StringField(required=False, max_length=60)
    Age = FloatField(min_value=0, required=False)
    UserName = StringField(required=False, max_length=200)
    Email = StringField(required=False, max_length=200)
    EmailVerified = BooleanField(default=False)
    PhoneNumber = StringField(required=False)
    PhoneVerified = BooleanField(default=False)
    Active = BooleanField(default=False)
    Roles = ListField(StringField(required=True), required=True)
    Password = StringField(required=False, max_length=200)
    DisplayPictureUrl = StringField(required=False, max_length=80)
    PublicUserId = StringField(required=False, max_length=32)
    LastLoginTime = DateTimeField(required=False)
    LogInCount = IntField(default=0, min_value=0)

    meta = {'collection': 'Users'}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.LastLoginTime = now()
