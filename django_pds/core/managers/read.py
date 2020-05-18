from .manager import BaseManager


class GenericReadManager(BaseManager):

    def read(self, document_name, q, page_size, page_number, order_by=None):

        if order_by is None:
            order_by = []

        if page_size > 100:
            page_size = 100
        if page_number < 1:
            page_number = 0
        else:
            page_number = page_number - 1

        try:
            data = self.get_document(document_name).objects.filter(q).order_by(*order_by).skip(
                page_size * page_number).limit(page_size)
            cnt = data.count()
            return data, cnt
        except:
            return [], 0

    def read_by_id(self, model, item_id):
        try:
            data = model.objects(ItemId=item_id)
            cnt = data.count()
            return data, cnt
        except:
            return [], 0
