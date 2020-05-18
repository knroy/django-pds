from django_pds.core.managers import RequiredManager


def required(*fields):
    def required_wrapper(func):
        def checking_required(*args, **kwargs):
            required_manager = RequiredManager()
            request = args[1]
            error, response = required_manager.required(request, *fields)
            if error:
                return response
            return func(*args, **kwargs)

        return checking_required

    return required_wrapper
