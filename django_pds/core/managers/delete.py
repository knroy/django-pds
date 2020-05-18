from .manager import BaseManager


class GenericDeleteCommandManager(BaseManager):

    def has_permission(self, document_name, document_id, user_id):
        try:
            Model = self.get_document(document_name)
            mod = Model.objects(ItemId=document_id, IdsAllowedToDelete=user_id)
            return mod.count() > 0
        except BaseException as e:
            return False

    def delete(self, document_name, document_id):

        base_instance = self.is_base_instance(document_name)
        simple_base_instance = self.is_simple_base_doc_instance(document_name)

        if not base_instance and not simple_base_instance:
            return True, 'Document type must be `BaseDocument` ' \
                         'or `SimpleBaseDocument` ' \
                         'from django_pds.core.base Module'

        try:
            Model = self.get_document(document_name)
            mod = Model.objects(ItemId=document_id)
            mod.delete()
            return True, "Delete success!"
        except BaseException as e:
            return False, str(e)

    def permission_and_delete(self, entity, user_id, item_id):
        if self.has_permission(entity, user_id, item_id):
            return self.delete(entity, item_id)
        return False
