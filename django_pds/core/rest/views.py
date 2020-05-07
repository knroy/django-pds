from rest_framework.views import APIView

from .exceptions import method_not_allowed


class BaseAPIView(APIView):

    def http_method_not_allowed(self, request, *args, **kwargs):
        return method_not_allowed()
