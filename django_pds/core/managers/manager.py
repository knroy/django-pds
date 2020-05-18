from django_pds.core.base import BaseDocument, SimpleBaseDocument
from django_pds.core.utils import get_document as document_provider


class BaseManager:

    def common_fields(self, a, b):
        return a.intersection(b)

    def get_document(self, document_name):
        return document_provider(document_name)

    def is_base_instance(self, document_name):
        doc = self.get_document(document_name)
        return issubclass(doc, BaseDocument)

    def is_simple_base_doc_instance(self, document_name):
        doc = self.get_document(document_name)
        return issubclass(doc, SimpleBaseDocument)
