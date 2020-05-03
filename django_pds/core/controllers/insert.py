import json

from django_pds.core.controllers.base import BaseController
from django_pds.core.settings import SECURITY_IDS_ATTRIBUTES, SECURITY_ROLES_ATTRIBUTES

OWNER = 'Owner'


class GenericInsertCommandController(BaseController):

    def __modify_ids(self, __defaults, user_id):
        items = []
        for _id in __defaults:
            if _id == OWNER:
                items.append(user_id)
            else:
                items.append(_id)
        return items

    def json_load(self, json_string):
        try:
            return False, json.loads(json_string)
        except BaseException as e:
            return True, str(e)

    def already_exists(self, document_name, document_id):
        try:
            data = self.get_document(document_name).objects(ItemId=document_id)
            return data.count() > 0
        except BaseException as e:
            return False

    def insert_one(self, document_name, data, default_permission, user_id):
        try:
            Model = self.get_document(document_name)
            mod = Model(**data)
            mod.CreatedBy = user_id
            mod.LastUpdateBy = user_id

            for item in SECURITY_ROLES_ATTRIBUTES:
                roles = default_permission.get(item, [])
                setattr(mod, item, roles)

            for item in SECURITY_IDS_ATTRIBUTES:
                ids = default_permission.get(item, [])
                ids = self.__modify_ids(ids, user_id)
                setattr(mod, item, ids)

            # Only Required on Entity Default Permission Settings for
            # Writing / Inserting Documents
            # Otherwise it's ok to insert EMPTY LIST
            setattr(mod, 'RolesAllowedToWrite', [])
            setattr(mod, 'IdsAllowedToWrite', [])

            mod.save()
            return False, mod.ItemId
        except BaseException as e:
            return True, e

    def insert_many(self, document_name, data_array, default_permission, user_id):
        results = []
        for data in data_array:
            err, item_id = self.insert_one(document_name, data, default_permission, user_id)
            if err:
                results.append(None)
            else:
                results.append(item_id)
        return results
