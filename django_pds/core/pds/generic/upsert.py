from django_pds.core.managers import GenericInsertCommandManager
from .update import data_update
from .write import data_insert


def data_upsert(document_name, data, user_id=None, ignore_security=False, force_upsert=False, track_error=False):
    try:
        insert_ctrl = GenericInsertCommandManager()
        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))

        if not already_exists:
            return data_insert(user_id, document_name, data, ignore_security, force_upsert, track_error)
        else:
            return data_update(user_id, document_name, data, ignore_security, track_error)

    except BaseException as e:
        return True, str(e)
