from django.http import JsonResponse


def server_error(request, *args, **kwargs):
    """
    Generic 500 error handler.
    """
    res = {
        "error_status": 500,
        "error": "server_error",
        "error_description": "Server has encountered an error 500"
    }
    return JsonResponse(res, status=500)


def access_denied(request):
    res = {
        "error_status": 401,
        "error": "access_permission_error",
        "error_description": "You don't have sufficient permission to access this specified HTTP URL"
    }
    return JsonResponse(res, status=401)


def url_not_found(request):
    res = {
        "error": "invalid_api_url",
        "error_status": 404,
        "error_message": "The specified HTTP URL is not valid."
    }
    return JsonResponse(res, status=404)


def method_not_allowed():
    res = {
        "error_status": 405,
        "error": "invalid_method",
        "error_description": "The specified HTTP method is not valid."
    }
    return JsonResponse(res, status=405)
