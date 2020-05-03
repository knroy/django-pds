from mongoengine import Q
from rest_framework import status
from rest_framework.response import Response

from django_pds.conf import settings
from django_pds.core.controllers import UserReadableDataController, GenericReadController, UserRoleMapsController
from django_pds.core.rest.response import error_response, success_response_with_total_records
from django_pds.core.utils import get_fields, get_document, is_abstract_document
from django_pds.serializers import GenericSerializerAlpha
from ..parser.query import QueryParser
from ..parser.terms import FILTER, WHERE, SELECT, PAGE_SIZE, PAGE_NUM, ORDER_BY, RAW_WHERE

NOT_SELECTABLE_ENTITIES_BY_PDS = settings.SELECT_NOT_ALLOWED_ENTITIES
SECURITY_ATTRIBUTES = settings.SECURITY_ATTRIBUTES


def get_by_sql_filter_api_view_helper(document_name, sql_text, user_id):
    """
    :param document_name:
    :param sql_text:
    :param user_id:
    :return:
    """

    document = get_document(document_name)

    # checking either model exists
    # or entity exists in not selectable entities

    if not document:
        return False, error_response('document model not found')

    if document_name in NOT_SELECTABLE_ENTITIES_BY_PDS:
        return False, error_response('document model is not selectable')

    if is_abstract_document(document_name):
        return False, error_response('document model not found')

    # checking for row level permission

    try:
        parser = QueryParser(sql_text)
        dictionary = parser.parse()

        # filtering fields in where clause
        _filters = []
        if dictionary.get(FILTER, None):
            _filters = dictionary[FILTER]

        security_attr = set(SECURITY_ATTRIBUTES)
        filter_fields = set(_filters)

        contains_security_attributes = filter_fields.intersection(security_attr)

        if len(contains_security_attributes) > 0:
            return True, error_response('Security attributes found in where clause')

        document_fields = set(get_fields(document_name))

        if len(filter_fields - document_fields) > 0:
            return True, error_response('Where clause contains unknown attribute to this Entity')

        # checking user readable data from database for this particular request

        fields = ['ItemId']
        if dictionary.get(SELECT, None):
            fields = dictionary[SELECT]

        urds_ctrl = UserReadableDataController()
        err, _fields = urds_ctrl.get_user_readable_data(document_name)

        if err:
            msg = f'Entity \'{document_name}\' is missing from user readable data\'s'
            return True, error_response(msg)

        diff = set(fields) - set(_fields.UserReadableFields)
        if len(diff) > 0:
            return True, error_response("Select clause contains unreadable attributes")

        sql_ctrl = GenericReadController()
        __raw__where = dictionary.get(RAW_WHERE, {})

        page_num = dictionary.get(PAGE_NUM, 1)
        page_size = dictionary.get(PAGE_SIZE, 10)

        q = Q()
        if dictionary.get(WHERE, None):
            q = dictionary[WHERE]

        urm_ctrl = UserRoleMapsController()
        roles = urm_ctrl.get_user_roles(user_id)

        q2 = Q(IdsAllowedToRead=user_id)
        for role in roles:
            q2 = q2.__or__(Q(RolesAllowedToRead=role))
        q = q.__and__(q2)

        order_by = []
        if dictionary.get(ORDER_BY, None):
            order_by = dictionary[ORDER_BY]

        data, cnt = sql_ctrl.read(document_name, q, page_size, page_num, order_by)
        if cnt == 0:
            res = success_response_with_total_records([], cnt)
            return Response(res, status=status.HTTP_200_OK)
        gsa = GenericSerializerAlpha(document_name=document_name)
        for field in fields:
            gsa.select(field)
        json = gsa.serialize(data)
        res = success_response_with_total_records(json.data, cnt)
        return False, res
    except BaseException as e:
        return True, error_response(str(e))
