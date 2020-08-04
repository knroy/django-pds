import json

from django.utils.timezone import now

from django_pds.core.utils import get_document
from .manager import BaseManager
from .userrolemaps import UserRoleMapsManager

ADMIN = "admin"


class GenericUpdateCommandManager(BaseManager):

    def json_load(self, json_string):
        try:
            return False, json.loads(json_string)
        except BaseException as e:
            return True, str(e)

    def already_exists(self, document_name, item_id):
        try:
            data = get_document(document_name).objects(ItemId=item_id)
            return data.count() > 0
        except BaseException as e:
            return False

    def can_update(self, document_name, item_id, user_id):

        data = get_document(document_name).objects(ItemId=item_id)
        if data.count() > 0:
            data = data[0]
            user_role_manager = UserRoleMapsManager()
            user_roles = set(user_role_manager.get_user_roles(user_id))
            permitted_roles = set(getattr(data, 'RolesAllowedToUpdate', []))
            permitted_ids = set(getattr(data, 'IdsAllowedToUpdate', []))
            permitted_roles.add(ADMIN)
            common_roles = user_roles.intersection(permitted_roles)
            return len(common_roles) > 0 or user_id in permitted_ids
        return False

    def update_one(self, document_name, data, user_id=None):
        try:

            base_instance = self.is_base_instance(document_name)
            simple_base_instance = self.is_simple_base_doc_instance(document_name)

            if not base_instance and not simple_base_instance:
                return True, 'Document type must be `BaseDocument` ' \
                             'or `SimpleBaseDocument` ' \
                             'from django_pds.core.base Module'

            Model = get_document(document_name)
            item_id = data.get('ItemId', None)
            _data = Model.objects(ItemId=item_id)

            if base_instance:
                data['LastUpdateDate'] = now()
                if user_id:
                    data['LastUpdateBy'] = user_id

            _data.update(**data)
            return False, _data[0].ItemId

        except BaseException as e:
            return True, e

    def update_many(self, document_name, data_array, user_id=None):
        results = []
        for data in data_array:
            err, item_id = self.update_one(document_name, data, user_id)
            if err:
                results.append(None)
            else:
                results.append(item_id)
        return results
