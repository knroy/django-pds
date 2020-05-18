from mongoengine import QuerySet


class PdsBaseQuerySet(QuerySet):

    def __has_delete_permission(self, document_id, user_id):
        docs = self.filter(ItemId=document_id, IdsAllowedToDelete=user_id)
        return docs.count() > 0

    def __pds_delete(self, document_id):
        docs = self.filter(ItemId=document_id)
        count = docs.delete()
        return count > 0

    def pds_delete(self, document_id, user_id):
        if self.__has_delete_permission(document_id, user_id):
            return self.__pds_delete(document_id)
        return False

    def exists(self, document_id):
        return self.filter(ItemId=document_id).count() > 0
