import traceback

from mongoengine import base


def is_abstract_model(model):
    return model._meta.get('abstract', False)


def get_document(document):
    try:
        return base.get_document(document)
    except BaseException as e:
        return None


def get_fields(model_name, with_auto_id=False):
    model = base.get_document(model_name)
    _fields = list(model._fields.keys())
    if not with_auto_id:
        elem = 'auto_id_0'
        if elem in _fields:
            _fields.remove(elem)
    return _fields


def origin(request):
    if request.META is not None:
        return request.META.get('HTTP_ORIGIN')
    return None


def get_host(request):
    host = origin(request)
    if host is None:
        return True, None
    replace = ['https://', 'http://', 'www.', '/']
    for item in replace:
        host = host.replace(item, '')
    hosts = host.split(':')
    return hosts[0]


def authorization_token(request):
    return request.META.get('HTTP_AUTHORIZATION', None)


def get_content_type(request):
    return request.META.get('CONTENT_TYPE', None)


def path(request):
    return str(request.META.get('PATH_INFO', ''))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def print_traceback():
    tb = traceback.format_exc()
    print(tb)
