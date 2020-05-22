from django.urls import include, re_path

urlpatterns = [
    re_path(r'^rest_api/', include('api.urls'))
]
