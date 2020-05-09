from django_pds.conf import settings
from django_pds.core.controllers import DefaultPermissionSettingsController
from django_pds.core.controllers import GenericInsertCommandController
from django_pds.core.rest.response import error_response, error_response_read_only_fields

security_attributes = settings.SECURITY_ATTRIBUTES
read_only_fields = settings.READ_ONLY_FIELDS


def simple_data_insert_api_view_helper(document_name, data_json, force_insert=False):

    insert_ctrl = GenericInsertCommandController()
    err, data = insert_ctrl.json_load(data_json)
    if err:
        return True, error_response(err)

    if not force_insert:
        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))
        if already_exists:
            return True, error_response(
                "document ItemId already exists, you can't create new collection "
                "with the same ItemId, if you want to update, "
                "use pds update helper or pds upsert helper")

    err, response = insert_ctrl.insert_one(document_name, data)

    if err:
        return True, error_response(response)
    return False, response


def data_insert_api_view_helper(document_name, data_json, user_id):
    entity_permission = DefaultPermissionSettingsController()

    can_insert = entity_permission.can_insert(document_name, user_id)

    if can_insert:

        insert_ctrl = GenericInsertCommandController()
        err, data = insert_ctrl.json_load(data_json)
        if err:
            return True, error_response(err)

        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))
        if already_exists:
            return True, error_response(
                "document ItemId already exists, you can't create new collection "
                "with the same ItemId, if you want to update, "
                "use pds update helper or pds upsert helper")

        data_fields = set(data.keys())

        rof = set(read_only_fields)
        common_fields = data_fields.intersection(rof)
        if len(common_fields) > 0:
            return True, error_response_read_only_fields(common_fields, "read only attributes found in json data")

        sec_attr = set(security_attributes)
        common_fields = data_fields.intersection(sec_attr)
        if len(common_fields) > 0:
            return True, error_response_read_only_fields(common_fields, "security attributes found in json data")

        # insert data after all the verification and security checking's

        error, permissions = entity_permission.get_document_name_permissions(document_name)
        if error:
            return False, error_response(error)

        err, response = insert_ctrl.insert_one(document_name, data, user_id, permissions)

        if err:
            return True, error_response(response)
        return False, response
    else:
        return True, error_response("access denied, you don't have sufficient permission to insert data")
