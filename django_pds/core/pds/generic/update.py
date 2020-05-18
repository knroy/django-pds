from django_pds.conf import settings
from django_pds.core.managers import GenericUpdateCommandManager

SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES
READ_ONLY_FIELDS = settings.READ_ONLY_FIELDS


def data_update(document_name, data, user_id=None, ignore_security=False):
    try:

        update_ctrl = GenericUpdateCommandManager()

        if ignore_security:
            return update_ctrl.update_one(document_name, data)

        data_fields = set(data.keys())
        security_attributes = set(SECURITY_ATTRIBUTES)
        common_fields = update_ctrl.common_fields(data_fields, security_attributes)

        if len(common_fields) > 0:
            fields = ','.join(common_fields)
            return True, f'the following security attributes {fields} found in the json data'

        read_only_fields = set(READ_ONLY_FIELDS)
        rof = update_ctrl.common_fields(data_fields, read_only_fields)
        if len(rof) > 0:
            fields = ','.join(rof)
            return True, f'the following read only attributes {fields} found in the json data'

        can_update = update_ctrl.can_update(document_name, data.get('ItemId', None), user_id)

        if can_update:
            return update_ctrl.update_one(document_name, data, user_id)
        else:
            return True, "access denied, you don't have sufficient permission to update"
    except BaseException as e:
        return True, str(e)
