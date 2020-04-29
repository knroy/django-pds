from rest_framework.views import APIView as AV

from .exceptions import method_not_allowed


class APIView(AV):

    def http_method_not_allowed(self, request, *args, **kwargs):
        return method_not_allowed()
