####  `CRUD :: INSERT`
<br>

let's start with defining a document schema `Patient`:

```python
from mongoengine import *
from django_pds.core.base import BaseDocument


class Patient(BaseDocument):
    name = StringField(required=True, max_length=80)
    age = IntField(min_value=0, required=True)
    contact = StringField(required=True, max_length=15)
```

**how about, controlling who can read, insert, delete and update a `Patient` record, although the read query coming from frontend?**

**`BaseDocument`** contains all the row level security attributes (**given below**). By **`Row Level Security`**, it means, every single individual document in a collection will contain its own security attributes, by which we will ensure by whom a document in a collection can be read, updated, inserted and deleted based on user id's and roles.

```python
IdsAllowedToRead = ListField(StringField(max_length=36), default=[])
IdsAllowedToWrite = ListField(StringField(max_length=36), default=[])
IdsAllowedToUpdate = ListField(StringField(max_length=36), default=[])
IdsAllowedToDelete = ListField(StringField(max_length=36), default=[])

RolesAllowedToRead = ListField(StringField(max_length=36), default=[])
RolesAllowedToWrite = ListField(StringField(max_length=36), default=[])
RolesAllowedToUpdate = ListField(StringField(max_length=36), default=[])
RolesAllowedToDelete = ListField(StringField(max_length=36), default=[])
```

We will get back to the explanation of requirements of these fields and use of these fields in a document. Let's get introduced with pre-defined models(documents) in `django-pds`. `django-pds` comes with some sophisticated pre-define documents:

```python
from django_pds.models import EntityDefaultPermissionSetting, UserRoleMap, UserReadableData
```

These pre-defined documents helps us to achieve `Row Level Security`. Why it's named `Row Level Security`? In a collection, we can imagine every single document as a Row. You can think of `Document Level Security` perhaps. 

How row level security is designed here in `django-pds`?

**To enable `Row Level Security` on a document, following conditions must be met:**

- The document should inherit (i.e document needs to be a subclass of) `BaseDocument` from `from django_pds.core.base import BaseDocument`
- There should be a document in `EntityDefaultPermissionSettings` collection containing the document name as `EntityName`
- There should be at least one document in `UserReadableDatas` collection specifying `Role` and `EntityName` which role from a particular document can read fields.
- Last, every single user created on this system, their one or multiple roles should have entry on `UserRoleMaps` collection.


***

##### Example of Achieving Row Level Security for `Patient` document:

***

i) insert permission settings document in `EntityDefaultPermissionSettings` collection for the `Patient` document:


```json
{
    "_id" : "7da1cebe-5c04-47bd-a3df-d68b5fdf34bf", 
    "EntityName" : "Patient", 
    "IdsAllowedToRead" : ["owner"], 
    "IdsAllowedToWrite" : ["owner"], 
    "IdsAllowedToUpdate" : ["owner"], 
    "IdsAllowedToDelete" : [], 
    "RolesAllowedToWrite" : ["doctor", "admin"],
    "RolesAllowedToRead" : [], 
    "RolesAllowedToUpdate" : [], 
    "RolesAllowedToDelete" : []
}
```

So, when a user tries to insert a `Patient` data, before everything else, security permission settings will be checked. You can see there is a string `owner` in `IdsAllowedToRead, IdsAllowedToWrite, IdsAllowedToDelete` fields. It's going to be converted into a user id after insertion happens. If a user is neither a `doctor` nor an `admin` won't be able to insert a `Patient` information. Because, we specified `RolesAllowedToWrite` is only `doctor` and `admin`.

ii) insert read permission settings document in `UserReadableDatas` collection for the `Patient` document:

```json
{
    "_id" : "f38f49fd-2915-470f-85ce-8e217c7b8822", 
    "EntityName" : "Patient", 
    "Role" : "doctor", 
    "UserReadableFields": ["ItemId", "name", "age", "contact"]
}
```
```json
{
    "_id" : "157f4edb-2dfe-4200-85f0-202abf5c1dc8", 
    "EntityName" : "Patient", 
    "Role" : "patient", 
    "UserReadableFields": ["ItemId", "name", "age", "contact"]
}
```
```json
{
    "_id" : "d248cfb9-304f-4ccb-9475-f9ab038da3ba", 
    "EntityName" : "Patient", 
    "Role" : "user", 
    "UserReadableFields": ["ItemId", "name", "contact"]
}
```
```json
{
    "_id" : "e3e450fc-4cc1-429e-8837-7df7b1c4962", 
    "EntityName" : "Patient", 
    "Role" : "default", 
    "UserReadableFields": ["ItemId", "name"]
}
```

`UserReadableDatas` ensure maximum readable fields for a particular role. If every single roles can read all the same fields, just instead of any role, use `default`. Don't put any security attributes in `UserReadableFields`, API won't let you read security attributes unless you override the default `django_pds` lazy loaded settings from `django_pds.conf`

Supposing `user_id` of the `doctor` or `admin` is : **`862bdaf0-6fa4-476e-be07-43ededfc222c`**. So, when a `doctor` or an `admin` inserts `Patient` data, it should be looking like this.

```json
{ 
    "_id" : "2e9fa69f-7180-4ddc-b25e-17fedb9872ab", 
    "CreatedBy" : "862bdaf0-6fa4-476e-be07-43ededfc222c", 
    "CreateDate" : ISODate("2020-04-21T16:49:13.980+0000"), 
    "Language" : "en-US", 
    "LastUpdateDate" : ISODate("2020-04-21T16:59:42.283+0000"), 
    "LastUpdateBy" : "862bdaf0-6fa4-476e-be07-43ededfc222c", 
    "Tags" : [], 
    "IdsAllowedToRead" : ["862bdaf0-6fa4-476e-be07-43ededfc222c"], 
    "IdsAllowedToWrite" : [], 
    "IdsAllowedToUpdate" : ["862bdaf0-6fa4-476e-be07-43ededfc222c"], 
    "IdsAllowedToDelete" : ["862bdaf0-6fa4-476e-be07-43ededfc222c"], 
    "RolesAllowedToRead" : [], 
    "RolesAllowedToWrite" : [], 
    "RolesAllowedToUpdate" : [], 
    "RolesAllowedToDelete" : [], 
    "name" : "John Doe", 
    "age" : 30,
    "contact" : "+15678082323"
}
```
