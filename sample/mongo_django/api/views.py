from rest_framework import status
from rest_framework.response import Response

from django_pds.core.pds.generic import data_read, basic_data_read, data_insert, data_update, data_delete
from django_pds.core.rest.decorators import required
from django_pds.core.rest.response import error_response, success_response
from django_pds.core.rest.views import BaseAPIView


class GenericDeleteRestAPI(BaseAPIView):

    # required decorator check request.data
    # before calling the post method for these required params
    @required("document_name", "document_id")
    def post(self, request):
        try:

            # we are expecting payload with the request

            document_name = request.data['document_name']
            document_id = request.data['document_id']

            # here the below user id is manually added
            # for demonstration purpose
            # you can extract an user id from the request
            # or from the jwt token if you implement
            user_id = '862bdaf0-6fa4-476e-be07-43ededfc222c'
            # user id is an optional parameter if you want to ignore security
            # if ignore_permission=True, then row level security will be ignored
            # permission checking will be disabled

            error, result = data_delete(document_name, document_id, user_id, ignore_permissions=False)

            if error:
                response = error_response(result)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            response = success_response(result)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            response = error_response(str(e))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RestInsert(BaseAPIView):

    # required decorator check request.data
    # before calling the post method for these required params
    @required("document_name", "data")
    def post(self, request):
        try:

            # we are expecting payload with the request

            document_name = request.data['document_name']
            data = request.data['data']

            # as we are not checking row level security,
            # ignoring offered row level security

            error, result = data_insert(document_name, data, ignore_security=True)

            if error:
                response = error_response(result)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            response = success_response(result)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            response = error_response(str(e))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RestUpdateAPIView(BaseAPIView):

    # required decorator check request.data
    # before calling the post method for these required params
    @required("document_name", "data")
    def post(self, request):
        try:

            # we are expecting payload with the request

            document_name = request.data['document_name']
            data = request.data['data']

            # here the below user id is manually added
            # for demonstration purpose
            # you can extract an user id from the request
            # or from the jwt token if you implement
            user_id = '862bdaf0-6fa4-476e-be07-43ededfc222c'
            # user id is an optional parameter if you want to ignore security
            # if ignore_security=True, then row level security will be ignored

            error, result = data_update(document_name, data, ignore_security=True, user_id=user_id)

            if error:
                response = error_response(result)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            response = success_response(result)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            response = error_response(str(e))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetBySQLFilter(BaseAPIView):

    required("document_name", "query")
    def post(self, request):

        try:
            params = request.data

            document_name = params['document_name']
            query = params['query']

            # here the below user id is manually added
            # for demonstration purpose
            # you can extract an user id from the request
            # or from the jwt token if you implement
            user_id = '862bdaf0-6fa4-476e-be07-43ededfc222c'

            error, data = data_read(document_name, query, user_id=user_id, readable=False, error_track=True)

            return Response(data, status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class GetBySQLFilter2(BaseAPIView):

    def get(self, request):

        try:

            document_name = 'Award'
            fields = ('ItemId', 'Title', 'Year', 'Description')
            error, data_or_exception = basic_data_read(document_name, fields=fields)
            return Response(data_or_exception, status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)


class BasicDataReadRestAPI(BaseAPIView):

    required("document_name", "fields")
    def post(self, request):

        try:

            document_name = request.data['document_name']
            fields = request.data['fields']
            page_size = request.data.get('pageSize', 10)  # optional params
            page_number = request.data.get('pageNumber', 1)  # optional params
            order_by = request.data.get('order_by', [])  # optional params
            error, data_or_exception = basic_data_read(document_name, fields=fields,
                                                       page_size=page_size, page_num=page_number,
                                                       order_by=order_by)
            return Response(data_or_exception,
                            status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
