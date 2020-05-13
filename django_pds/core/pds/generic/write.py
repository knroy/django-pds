from django_pds.conf import settings
from django_pds.core.controllers import DefaultPermissionSettingsController
from django_pds.core.controllers import GenericInsertCommandController

security_attributes = settings.SECURITY_ATTRIBUTES
read_only_fields = settings.READ_ONLY_FIELDS


def data_insert(document_name, data, user_id=None, ignore_security=False, force_insert=False):

    insert_ctrl = GenericInsertCommandController()

    if force_insert:
        already_exists = insert_ctrl.already_exists(document_name, data.get('ItemId', None))
        if already_exists and not force_insert:
            return True, "document ItemId already exists, you can't create new collection " \
                         "with the same ItemId, if you want to update, " \
                         "use pds update or upsert method"

    if ignore_security:
        return insert_ctrl.insert_one(document_name, data)

    entity_permission = DefaultPermissionSettingsController()
    can_insert = entity_permission.can_insert(document_name, user_id)

    if can_insert:

        data_fields = set(data.keys())
        rof = set(read_only_fields)
        common_fields = data_fields.intersection(rof)
        if len(common_fields) > 0:
            fields = ','.join(common_fields)
            return True, f'the following read only attributes {fields} found in the json data'
        sec_attr = set(security_attributes)
        common_fields = data_fields.intersection(sec_attr)
        if len(common_fields) > 0:
            fields = ','.join(common_fields)
            return True, f'following security attributes {fields} found in the json data'
        # insert data after all the verification and security checking's
        error, permissions = entity_permission.get_document_name_permissions(document_name)
        if error:
            return True, error
        return insert_ctrl.insert_one(document_name, data, user_id, permissions)
    else:
        return True, "access denied, you don't have sufficient permission to insert data"
