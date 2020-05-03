DEFAULT_USER_ROLE = 'user'

SYSTEM_SUPPORTED_ROLES = [
    "admin",
    "user",
    "anonymous"
]

SECURITY_ATTRIBUTES = [
    'IdsAllowedToRead', 'IdsAllowedToWrite', 'IdsAllowedToUpdate', 'IdsAllowedToDelete',
    'RolesAllowedToRead', 'RolesAllowedToWrite', 'RolesAllowedToUpdate', 'RolesAllowedToDelete'
]

SECURITY_ROLES_ATTRIBUTES = [
    'RolesAllowedToRead', 'RolesAllowedToWrite', 'RolesAllowedToUpdate', 'RolesAllowedToDelete'
]

SECURITY_IDS_ATTRIBUTES = [
    'IdsAllowedToRead', 'IdsAllowedToWrite', 'IdsAllowedToUpdate', 'IdsAllowedToDelete',
]

READ_ONLY_FIELDS = ['CreatedBy', 'CreateDate', 'LastUpdateDate', 'LastUpdateBy']

# bundled default models available in django_pds

DOCUMENT_ENTITY = 'Entity'
DOCUMENT_ROLE = 'Role'
DOCUMENT_ENTITY_DEFAULT_PERMISSION_SETTING = 'EntityDefaultPermissionSetting'
DOCUMENT_USER = 'User'
DOCUMENT_USER_READABLE_DATA = 'UserReadableData'
DOCUMENT_USER_ROLE_MAPS = 'UserRoleMap'

# JWT Token configurations

# JWT_TOKEN_SECRET_KEY add this on your custom settings
JWT_TOKEN_EXPIRATION_TIME = 6  # 6 min
JWT_TOKEN_AUDIENCE = '*'
JWT_TOKEN_ALGORITHM = 'HS256'

SELECT_NOT_ALLOWED_ENTITIES = [
    'User', 'UserReadableData', 'Tenant', 'Entity',
    'EntityDefaultPermissionSetting', 'Role', 'UserReadableData', 'UserRoleMap'
]

READ_NOT_ALLOWED_ATTRIBUTES = [
    'CreatedBy', 'LastUpdateBy', 'IdsAllowedToRead', 'IdsAllowedToWrite', 'IdsAllowedToUpdate',
    'IdsAllowedToDelete', 'RolesAllowedToRead', 'RolesAllowedToWrite', 'RolesAllowedToUpdate', 'RolesAllowedToDelete'
]

MONGO_ENGINE_USABLE_OPERATORS = [
    'ne', 'lt', 'lte', 'gt', 'in', 'nin', 'mod', 'all', 'size', 'exists', 'exact', 'iexact', 'contains', 'icontains',
    'startswith', 'istartswith', 'endswith', 'iendswith', 'match'
]

EDIT_NOT_ALLOWED_ATTRIBUTES_PDS = [
    'CreatedBy', 'CreateDate', 'LastUpdateDate', 'LastUpdateBy', 'IdsAllowedToRead', 'IdsAllowedToWrite',
    'IdsAllowedToUpdate', 'IdsAllowedToDelete', 'RolesAllowedToRead', 'RolesAllowedToWrite', 'RolesAllowedToUpdate',
    'RolesAllowedToDelete'
]
