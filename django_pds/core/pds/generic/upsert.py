from django_pds.core.controllers import GenericInsertCommandController
from django_pds.core.rest.response import error_response
from .update import data_update_api_view_helper
from .write import data_insert_api_view_helper


def data_upsert_api_view_helper(user_id, document_name, json_string):
    try:
        insert_ctrl = GenericInsertCommandController()
        err, data = insert_ctrl.json_load(json_string)
        if err:
            return True, error_response(err)

        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))

        if not already_exists:
            return data_insert_api_view_helper(user_id, document_name, json_string)
        else:
            return data_update_api_view_helper(user_id, document_name, json_string)

    except BaseException as e:
        return True, error_response(e)
