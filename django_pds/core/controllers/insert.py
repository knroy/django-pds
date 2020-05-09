import json

from django_pds.conf import settings
from django_pds.core.controllers.base import BaseController

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

    def insert_one(self, document_name, data, user_id=None, default_permission=None):
        try:
            Model = self.get_document(document_name)
            mod = Model(**data)

            if self.is_base_instance(document_name):

                if user_id:
                    mod.CreatedBy = user_id
                    mod.LastUpdateBy = user_id
                    for item in settings.SECURITY_IDS_ATTRIBUTES:
                        ids = default_permission.get(item, [])
                        ids = self.__modify_ids(ids, user_id)
                        setattr(mod, item, ids)

                if default_permission:
                    for item in settings.SECURITY_ROLES_ATTRIBUTES:
                        roles = default_permission.get(item, [])
                        setattr(mod, item, roles)

                    # Only Required on Entity Default Permission Settings for
                    # Writing / Inserting Documents
                    # Otherwise it's ok to insert EMPTY LIST

                    setattr(mod, 'RolesAllowedToWrite', [])
                    setattr(mod, 'IdsAllowedToWrite', [])

                mod.save()
                return False, mod.ItemId
            else:
                mod.save()
                return False, 'Inserted'

        except BaseException as e:
            return True, e

    def insert_many(self, document_name, data_array, user_id=None, default_permission=None):
        results = []
        for data in data_array:
            err, item_id = self.insert_one(document_name, data, user_id, default_permission)
            if err:
                results.append(None)
            else:
                results.append(item_id)
        return results
