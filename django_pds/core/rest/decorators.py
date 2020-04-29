from django_pds.core.controllers.base import RequiredController


def required(*fields):
    def required_wrapper(func):
        def checking_required(*args, **kwargs):
            required_ctrl = RequiredController()
            request = args[1]
            error, response = required_ctrl.required(request, *fields)
            if error:
                return response
            return func(*args, **kwargs)

        return checking_required

    return required_wrapper
