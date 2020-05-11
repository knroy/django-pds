from django_pds.core.controllers import GenericInsertCommandController
from .update import data_update
from .write import data_insert


def data_upsert(document_name, data_json, user_id=None, ignore_security=False, force_insert=False):
    try:
        insert_ctrl = GenericInsertCommandController()
        err, data_or_error = insert_ctrl.json_load(data_json)
        if err:
            return True, data_or_error

        data = data_or_error
        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))

        if not already_exists:
            return data_insert(user_id, document_name, data_json, ignore_security, force_insert)
        else:
            return data_update(user_id, document_name, data_json, ignore_security)

    except BaseException as e:
        return True, str(e)
