from django.conf import settings


class Settings(object):

    @property
    def SESSION_MIDDLEWARE_EXEMPT_URLS(self):
        return getattr(settings, 'TOKEN_EXEMPT_URLS', [])

    @property
    def AUTH_NOT_REQUIRED_URLS(self):
        return getattr(settings, 'AUTH_NOT_REQUIRED_URLS', [])


conf = Settings()
