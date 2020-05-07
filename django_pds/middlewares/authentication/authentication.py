import jwt
from django.core.cache import cache
from django.middleware.http import MiddlewareMixin

from django_pds.conf import settings
from django_pds.core.rest.exceptions import access_denied, server_error
from django_pds.core.utils import authorization_token, path
from .settings import conf

TOKEN_MISSING = 'Authorization token not found in the request headers'
INVALID_TOKEN = 'Invalid authentication token'
ACCESS_DENIED = 'Access denied'
TOKEN_AUTH_KEY_NOT_SET = 'Token secret key not set'

audience = settings.JWT_TOKEN_AUDIENCE
algorithm = settings.JWT_TOKEN_ALGORITHM
auth_key = getattr(settings, 'JWT_TOKEN_SECRET_KEY', None)


class AuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):

        url = path(request)

        if not auth_key:
            return server_error(request, message=TOKEN_AUTH_KEY_NOT_SET)

        bearer_token = authorization_token(request)

        flag = True

        for exempt_url in conf.SESSION_MIDDLEWARE_EXEMPT_URLS:
            if url.endswith(exempt_url):
                flag = False

        if not flag:
            return None

        if bearer_token is None:
            return access_denied(request, TOKEN_MISSING)

        try:

            token_hash = str(hash(bearer_token))
            payload = cache.get(token_hash)

            if payload is None:
                token = bearer_token.split()
                payload = jwt.decode(token[1], auth_key, audience=audience, unicode='utf-8', algorithms=algorithm)
                if payload is None:
                    return access_denied(request, message=INVALID_TOKEN)

            auth = payload.get('logged_in', False)

            for exempt_url in conf.AUTH_NOT_REQUIRED_URLS:
                if url.endswith(exempt_url):
                    auth = True

            if auth:
                return None
            else:
                return access_denied(request, ACCESS_DENIED)
        except BaseException as e:
            return access_denied(request, str(e))
