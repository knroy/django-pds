def error_response(message=None, status=None):
    return {
        "error_status": status or 400,
        "error": "bad_request",
        "error_description": message or "The request is not valid."
    }


def success_response(data=None, message=None, status=None):
    return {
        "success_status": status or 200,
        "error": None,
        "success_description": message or "request valid",
        "responsible": data or None
    }


def error_response_read_only_fields(fields, message=None, status=None):
    return {
        "error_status": status or 400,
        "error": "bad_request",
        "error_description": message or "The request is not valid.",
        "responsible": fields
    }


def success_response_with_total_records(data, count, message=None, status=None):
    return {
        "success_status": status or 200,
        "error": None,
        "success_description": message or "request valid",
        "results": data,
        "total_records": count
    }
