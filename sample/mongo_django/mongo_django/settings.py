import os

import mongoengine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '6c8+rfm8e6#bt&13$+4#(btshtf7#^)y3e@58=lzrxd5j4%q(m'

DEBUG = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None
}


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_pds',
    'api'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_pds.middlewares.UrlPathExistsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

ROOT_URLCONF = 'mongo_django.urls'

TEMPLATES = []

WSGI_APPLICATION = 'mongo_django.wsgi.application'

DATABASES = {}

# connecting to mongodb

DATABASE_NAME = '89595B8A-13EE-43F3-9D06-0D34D71D161B'

mongoengine.connect(DATABASE_NAME)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
