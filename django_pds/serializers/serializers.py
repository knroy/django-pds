from mongoengine import base
from mongoengine.queryset.queryset import QuerySet
from rest_framework_mongoengine import serializers


class GenericSerializerAlpha:
    __fields = ()
    __document = None

    def __init__(self, document_name=None, fields=None):
        if document_name:
            self.__document = base.get_document(document_name)
        if fields:
            self.__fields = fields

    def fields(self, fields='__all__'):
        self.__fields = fields
        return self

    def model(self, model):
        self.__document = model
        return self

    def document(self, document_name):
        self.__document = base.get_document(document_name)
        return self

    def delete(self):
        self.__del__()

    def __del__(self):
        pass

    def select(self, field):
        if type(self.__fields) == tuple:
            self.__fields = self.__fields + (field,)
        else:
            self.__fields = (field,)
        return self

    def select_all(self):
        self.__fields = '__all__'
        return self

    def serialize(self, data, many=True, allow_null=True):

        if type(data) is not QuerySet:
            many = False

        resp = self._GenSerializerAlpha(data, many=many, allow_null=allow_null, fields=self.__fields,
                                        document=self.__document)
        return resp

    class _GenSerializerAlpha(serializers.DocumentSerializer):

        def __init__(self, *args, **kwargs):
            __fields = kwargs.pop('fields', '__all__')
            __document = kwargs.pop('document', None)
            super(GenericSerializerAlpha._GenSerializerAlpha, self).__init__(*args, **kwargs)
            self.Meta.fields = __fields
            self.Meta.model = __document

        class Meta:
            model = None
            fields = '__all__'
