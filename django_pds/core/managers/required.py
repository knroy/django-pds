from rest_framework import status
from rest_framework.response import Response

from django_pds.core.rest.response import error_response


class RequiredManager:

    def required(self, request, *args):

        if request.META.get('REQUEST_METHOD') == 'GET':
            if len(args) > 0:
                response = error_response('Get method should not have required parameters. Config error.', status=400)
                return True, Response(response, status=status.HTTP_400_BAD_REQUEST)
        params, files = request.data, request.FILES
        required_fields = args
        missing_fields = []

        if len(required_fields) == 0:
            return False, None

        ignore_on_files = []

        for field in required_fields:
            if params.get(field) is None:
                missing_fields.append(field)
            else:
                ignore_on_files.append(field)

        for field in required_fields:
            if files.get(field) is None:
                if field not in ignore_on_files and field not in missing_fields:
                    missing_fields.append(field)

        if len(missing_fields) == 0:
            return False, None

        response = {
            "error": 400,
            "error_message": "missing required payload fields in this request",
            "missing_fields": missing_fields
        }

        return True, Response(response, status=status.HTTP_400_BAD_REQUEST)
