from django_pds.core.managers import DefaultPermissionSettingsManager, GenericDeleteCommandManager


def data_delete(document_name, document_id, user_id=None, ignore_permissions=False):
    try:

        delete_manager = GenericDeleteCommandManager()

        if ignore_permissions:
            return delete_manager.delete(document_name, document_id)

        entity_permission = DefaultPermissionSettingsManager()
        role_can_delete = False
        if user_id:
            role_can_delete = entity_permission.can_delete(document_name, user_id)
        id_can_delete = False
        if not role_can_delete and not user_id:
            id_can_delete = delete_manager.has_permission(document_name, user_id, document_id)
        if role_can_delete or id_can_delete:
            return delete_manager.delete(document_name, document_id)
        else:
            return True, "you don't have sufficient permission to delete"
    except BaseException as e:
        return True, str(e)
