from rest_framework import status
from rest_framework.response import Response

from django_pds.conf import settings
from django_pds.core.controllers import DefaultPermissionSettingsController
from django_pds.core.controllers import GenericInsertCommandController
from django_pds.core.rest.response import error_response, error_response_read_only_fields, success_response

READ_ONLY_FIELDS = settings.READ_ONLY_FIELDS


def data_insert_api_view_helper(user_id, document_name, json_string):
    """
    :param user_id: user_id is needed for security checking
    either the user have sufficient permission to insert data
    :param document_name: document name required for loading model
    :param json_string: json string is the json dumped data of collection data to be inserted
    :return: a tuple containing error and response
    first variable of tuple will be error: boolean -> True / False
    second element of the tuple will be the response -> success response / error response
    maintained standard procedure of responses
    """

    entity_permission = DefaultPermissionSettingsController()

    can_insert = entity_permission.can_insert(document_name, user_id)

    if can_insert:

        insert_ctrl = GenericInsertCommandController()
        err, data = insert_ctrl.json_load(json_string)
        if err:
            return True, error_response(err)

        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))
        if already_exists:
            return True, error_response(
                "document ItemId already exists, you can't create new collection "
                "with the same ItemId, if you want to update, "
                "use pds update helper or pds upsert helper")

        e, permissions = entity_permission.get_document_name_permissions(document_name)
        if e:
            res = error_response(e)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        permission_fields = set(permissions.keys())
        data_fields = set(data.keys())
        common_fields = data_fields.intersection(permission_fields)
        rof = insert_ctrl.common_fields(data_fields, set(READ_ONLY_FIELDS))
        if len(common_fields) > 0 or len(rof) > 0:
            return True, error_response_read_only_fields(common_fields, "read only attributes found in json data")

        # insert data after all the verification and security checking's

        err, response = insert_ctrl.insert_one(document_name, data, permissions, user_id)

        if err:
            return True, error_response(response)
        return False, success_response(response)
    else:
        return True, "access denied, you don't have sufficient permission to insert data"
