__all__ = [
    'InsertPermissionError',
    'UpdatePermissionError',
    'ReadPermissionError',
    'DeletePermissionError'
]


class PdsPermissionError(Exception):
    pass


class InsertPermissionError(PdsPermissionError):
    pass


class ReadPermissionError(PdsPermissionError):
    pass


class DeletePermissionError(PdsPermissionError):
    pass


class UpdatePermissionError(PdsPermissionError):
    pass
