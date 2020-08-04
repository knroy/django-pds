from django_pds.conf import settings
from django_pds.core.managers import GenericUpdateCommandManager
from django_pds.core.utils import print_traceback

SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES
READ_ONLY_FIELDS = settings.READ_ONLY_FIELDS


def data_update(document_name, data, user_id=None, ignore_security=False, track_error=False):
    results = []

    data_array = []
    if isinstance(data, dict):
        data_array.append(data)
    if isinstance(data, list):
        data_array = data

    update_manager = GenericUpdateCommandManager()

    for d in data_array:

        try:

            if ignore_security:
                error, res = update_manager.update_one(document_name, d)
                results.append({
                    "error": error,
                    "message": res
                })
                continue

            data_fields = set(d.keys())
            security_attributes = set(SECURITY_ATTRIBUTES)
            common_fields = update_manager.common_fields(data_fields, security_attributes)

            if len(common_fields) > 0:
                fields = ','.join(common_fields)
                results.append({
                    "error": True,
                    "message": f'following security attributes {fields} found in the json data'
                })
                continue

            read_only_fields = set(READ_ONLY_FIELDS)
            rof = update_manager.common_fields(data_fields, read_only_fields)
            if len(rof) > 0:
                fields = ','.join(rof)
                results.append({
                    "error": True,
                    "message": f'the following read only attributes {fields} found in the json data'
                })
                continue

            can_update = update_manager.can_update(document_name, d.get('ItemId', None), user_id)

            if can_update:
                err, res = update_manager.update_one(document_name, d, user_id)
                results.append({
                    "error": err,
                    "message": res
                })
            else:
                results.append({
                    "error": True,
                    "message": "access denied, you don't have sufficient permission to update"
                })

        except BaseException as e:

            if track_error:
                print_traceback()

            results.append({
                "error": True,
                "message": str(e)
            })
