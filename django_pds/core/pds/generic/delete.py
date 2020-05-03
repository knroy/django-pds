from django_pds.core.controllers import DefaultPermissionSettingsController, GenericDeleteCommandController

from django_pds.core.rest.response import success_response, error_response


def data_delete_api_view_helper(document_name, document_id, user_id):
    try:

        entity_permission = DefaultPermissionSettingsController()
        delete_ctrl = GenericDeleteCommandController()

        role_can_delete = entity_permission.can_delete(document_name, user_id)
        id_can_delete = False
        if not role_can_delete:
            id_can_delete = delete_ctrl.has_permission(document_name, user_id, document_id)

        if role_can_delete or id_can_delete:
            done = delete_ctrl.delete(document_name, document_id)
            if not done:
                return True, error_response('Delete command failed')
            return False, success_response("Delete success!")
        else:
            return True, error_response("you don't have sufficient permission to delete")
    except BaseException as e:
        return True, error_response(e)
