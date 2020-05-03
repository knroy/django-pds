from django_pds.core.controllers.base import BaseController


class GenericDeleteCommandController(BaseController):

    def has_permission(self, document_name, document_id, user_id):
        try:
            Model = self.get_document(document_name)
            mod = Model.objects(ItemId=document_id, IdsAllowedToDelete=user_id)
            return mod.count() > 0
        except BaseException as e:
            return False

    def delete(self, document_name, document_id):
        try:
            Model = self.get_document(document_name)
            mod = Model.objects(ItemId=document_id)
            mod.delete()
            return True
        except BaseException as e:
            return False

    def permission_and_delete(self, entity, user_id, item_id):
        if self.has_permission(entity, user_id, item_id):
            return self.delete(entity, item_id)
        return False
