from mongoengine import Q

from django_pds.conf import settings
from django_pds.core.controllers import UserReadableDataController, GenericReadController, UserRoleMapsController
from django_pds.core.rest.response import error_response, success_response_with_total_records
from django_pds.core.utils import get_fields, get_document, is_abstract_document
from django_pds.core.utils import print_traceback
from django_pds.serializers import GenericSerializerAlpha
from ..parser.query import QueryParser
from ..parser.terms import FILTER, WHERE, SELECT, PAGE_SIZE, PAGE_NUM, ORDER_BY, RAW_WHERE

NOT_SELECTABLE_ENTITIES_BY_PDS = settings.SELECT_NOT_ALLOWED_ENTITIES
SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES


def basic_data_read(document_name, fields='__all__',
                    page_size=10, page_num=1, order_by=None,
                    include_security_fields=False,
                    error_track=False):
    try:

        document = get_document(document_name)

        if not document or not document_name:
            return True, error_response(f'document by name `{document_name}` does\'t exists')

        if fields != '__all__' and not isinstance(fields, (list, tuple)):
            return True, error_response('fields must be a list or tuple')

        sql_ctrl = GenericReadController()
        data, cnt = sql_ctrl.read(document_name, Q(), page_size, page_num, order_by)
        if cnt == 0:
            return False, success_response_with_total_records([], cnt)
        gsa = GenericSerializerAlpha(document_name=document_name)
        if not fields == '__all__':
            for field in fields:
                gsa.select(field)
        else:
            fields = get_fields(document_name)
            if not include_security_fields:
                fields = tuple(set(fields) - set(SECURITY_ATTRIBUTES))
            gsa.fields(fields)

        json = gsa.serialize(data)
        res = success_response_with_total_records(json.data, cnt)
        return False, res
    except BaseException as e:
        if error_track:
            print_traceback()
        return True, error_response(str(e))


def data_read(
        document_name, sql_text, user_id=None,
        roles=None, checking_roles=True,
        readable=True, security_attributes=True,
        selectable=True, read_all=False, exclude_default=False,
        page_number=1, _size=10, error_track=False):
    """
    :param page_number:
    :param _size:
    :param checking_roles:
    :param document_name:
    :param sql_text:
    :param user_id:
    :param roles:
    :param readable:
    :param security_attributes:
    :param selectable:
    :param read_all:
    :return:
    """

    document = get_document(document_name)

    # checking either model exists
    # or entity exists in not selectable entities

    if not document:
        return False, error_response('document model not found')

    if is_abstract_document(document_name):
        return False, error_response('document model not found')

    if selectable and document_name in NOT_SELECTABLE_ENTITIES_BY_PDS:
        return False, error_response('document model is not selectable')

    try:
        parser = QueryParser(sql_text)
        dictionary = parser.parse()

        # filtering fields in where clause
        _filters = []
        if dictionary.get(FILTER, None):
            _filters = dictionary[FILTER]

        filter_fields = set(_filters)
        document_fields = set(get_fields(document_name))

        if len(filter_fields - document_fields) > 0:
            return True, error_response('Where clause contains unknown attribute to this Document')

        if security_attributes:
            security_attr = set(SECURITY_ATTRIBUTES)
            contains_security_attributes = filter_fields.intersection(security_attr)
            if len(contains_security_attributes) > 0:
                return True, error_response('Security attributes found in where clause')

        # checking user readable data from database for this particular request

        fields = ['ItemId']
        if dictionary.get(SELECT, None):
            fields = dictionary[SELECT]
        if read_all:
            fields = document_fields

        urm_ctrl = UserRoleMapsController()

        if readable:
            urds_ctrl = UserReadableDataController()
            __roles = None
            if user_id and not roles:
                __roles = urm_ctrl.get_user_roles(user_id)
            err, _fields = urds_ctrl.get_user_readable_data_fields(document_name, __roles, exclude_default)
            if err:
                msg = f'Entity \'{document_name}\' is missing from user readable data\'s'
                return True, error_response(msg)

            diff = set(fields) - _fields  # _fields are already a set
            if len(diff) > 0:
                return True, error_response("Select clause contains non readable attributes")

        sql_ctrl = GenericReadController()
        __raw__where = dictionary.get(RAW_WHERE, {})

        page_num = dictionary.get(PAGE_NUM, page_number)
        page_size = dictionary.get(PAGE_SIZE, _size)

        q = Q()
        if dictionary.get(WHERE, None):
            q = dictionary[WHERE]

        # checking for row level permission starts

        q2 = Q()

        if user_id:
            q2 = Q(IdsAllowedToRead=user_id)

        if checking_roles:
            if not roles and user_id:
                roles = urm_ctrl.get_user_roles(user_id)
            if roles and not isinstance(roles, (list, tuple)):
                return True, error_response('roles must be a list or a tuple.')
            for role in roles:
                q2 = q2.__or__(Q(RolesAllowedToRead=role))

        if user_id or (checking_roles and roles):
            q = q.__and__(q2)

        # checking for row level permission ends

        order_by = []
        if dictionary.get(ORDER_BY, None):
            order_by = dictionary[ORDER_BY]

        data, cnt = sql_ctrl.read(document_name, q, page_size, page_num, order_by)
        if cnt == 0:
            return False, success_response_with_total_records([], cnt)
        gsa = GenericSerializerAlpha(document_name=document_name)
        for field in fields:
            gsa.select(field)
        json = gsa.serialize(data)
        res = success_response_with_total_records(json.data, cnt)
        return False, res
    except BaseException as e:
        if error_track:
            print_traceback()
        return True, error_response(str(e))
