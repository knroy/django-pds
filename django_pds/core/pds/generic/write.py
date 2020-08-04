from django_pds.conf import settings
from django_pds.core.managers import DefaultPermissionSettingsManager, GenericInsertCommandManager
from django_pds.core.utils import print_traceback

security_attributes = settings.SECURITY_ATTRIBUTES
read_only_fields = settings.READ_ONLY_FIELDS


def data_insert(document_name, data, user_id=None, ignore_security=False, force_insert=False, track_error=False):
    results = []
    insert_manager = GenericInsertCommandManager()

    data_array = []

    if isinstance(data, dict):
        data_array.append(data)
    elif isinstance(data, list):
        data_array = data

    for d in data_array:

        try:

            if force_insert:
                already_exists = insert_manager.already_exists(document_name, d.get('ItemId', None))
                if already_exists and not force_insert:
                    message = "document ItemId already exists, you can't create new collection " \
                              "with the same ItemId, if you want to update, " \
                              "use pds update or upsert method"
                    results.append({
                        'error': True,
                        'message': message
                    })
                    continue

            if ignore_security:
                error, response = insert_manager.insert_one(document_name, d)
                results.append({
                    "error": error,
                    "message": response
                })
                continue

            entity_permission = DefaultPermissionSettingsManager()
            can_insert = entity_permission.can_insert(document_name, user_id)

            if can_insert:

                data_fields = set(d.keys())
                rof = set(read_only_fields)
                common_fields = data_fields.intersection(rof)
                if len(common_fields) > 0:
                    fields = ','.join(common_fields)
                    results.append({
                        "error": True,
                        "message": f'the following read only attributes {fields} found in the json data'
                    })
                    continue
                sec_attr = set(security_attributes)
                common_fields = data_fields.intersection(sec_attr)
                if len(common_fields) > 0:
                    fields = ','.join(common_fields)
                    results.append({
                        "error": True,
                        "message": f'following security attributes {fields} found in the json data'
                    })
                    continue
                # insert data after all the verification and security checking's
                error, permissions = entity_permission.get_document_name_permissions(document_name)
                if error:
                    results.append({
                        "error": error,
                        "message": permissions
                    })
                    continue
                err, response = insert_manager.insert_one(document_name, d, user_id, permissions)
                results.append({
                    "error": err,
                    "message": response
                })
            else:
                results.append({
                    "error": True,
                    "message": "access denied, you don't have sufficient permission to insert data"
                })
        except BaseException as e:
            if track_error:
                print_traceback()
            results.append({
                "error": True,
                "message": str(e)
            })
