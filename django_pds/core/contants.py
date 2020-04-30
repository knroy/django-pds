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

ROLE_ADMIN = "admin"
ROLE_OWNER = "owner"

READ_ONLY_FIELDS = ['CreatedBy', 'CreateDate', 'LastUpdateDate', 'LastUpdateBy']

DOCUMENT_ENTITY = 'Entity'
DOCUMENT_ROLE = 'Role'
DOCUMENT_USER_READABLE_DATA = 'UserReadableData'
DOCUMENT_USER_ROLE_MAPS = 'UserRoleMap'

