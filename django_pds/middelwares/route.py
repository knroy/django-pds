from django.middleware.http import MiddlewareMixin
from django.urls import resolve
from django.urls.resolvers import Resolver404

from django_pds.core.rest.exceptions import url_not_found


class UrlPathExistsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            resolve(request.path)
            return None
        except Resolver404:
            return url_not_found(request)
