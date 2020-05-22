
from django.urls import re_path

from .views import GetBySQLFilter, GetBySQLFilter2
from .views import RestInsert

urlpatterns = [
    re_path(r'^read$', GetBySQLFilter.as_view(), name='sql test'),
    re_path(r'^sql-filter$', GetBySQLFilter2.as_view(), name='sql test 2'),
    re_path(r'^insert$', RestInsert.as_view(), name='rest api insert'),
]