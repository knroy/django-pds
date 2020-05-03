from django_pds.conf import settings
from django_pds.core.controllers import GenericUpdateCommandController
from django_pds.core.rest.response import error_response, success_response, error_response_read_only_fields

SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES
READ_ONLY_FIELDS = settings.READ_ONLY_FIELDS


def data_update_api_view_helper(user_id, document_name, json_string):
    try:

        update_ctrl = GenericUpdateCommandController()
        err, data = update_ctrl.json_load(json_string)

        if err:
            return True, error_response(err)

        can_update = update_ctrl.can_update(document_name, data.get('ItemId', None), user_id)

        if can_update:

            read_only_permission_fields = set(SECURITY_ATTRIBUTES)
            data_fields = set(data.keys())
            common_fields = update_ctrl.common_fields(data_fields, read_only_permission_fields)
            common_fields_2 = update_ctrl.common_fields(data_fields, set(READ_ONLY_FIELDS))
            if len(common_fields) > 0 or len(common_fields_2):
                return True, error_response_read_only_fields(common_fields)

            # update data after all the verification and security checking's

            err, response = update_ctrl.update_one(document_name, data, user_id)

            if err:
                return err, error_response(response)

            return False, success_response(response)
        else:
            return True, error_response("access denied, you don't have sufficient permission to update")
    except BaseException as e:
        return True, error_response(e)
