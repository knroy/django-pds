`django-pds` has two pre-defined document schema. `SimpleBaseDocument` and `BaseDocument`

`SimpleBaseDocument` contains only `ItemId` (an alias of `_id` of MongoDB index field) and doesn't contain [Row Level Security](https://github.com/knroy/django-pds/wiki/Row-Level-Security) fields and `BaseDocument` contains all the [Row Level Security](https://github.com/knroy/django-pds/wiki/Row-Level-Security) fields.

**Reason of two different base document:**

1. to be consistent with the use of generic `data_insert`, `data_update`, `data_delete` and `data_upsert` methods from `django_pds.core.pds.generic`
2. while defining a document, you must have to inherit either from `SimpleBaseDocument` or from `BaseDocument` from `django_pds.core.base` to use `data_insert`, `data_update`, `data_delete` and `data_upsert` methods from `django_pds.core.pds.generic`

**Data Insertion with `BaseDocument`:**

let's define a document schema `BlogPost`:

```python
from mongoengine import StringField, ListField, IntField

from django_pds.core.base import BaseDocument


class BlogPost(BaseDocument):
    Title = StringField(max_length=2000, required=True)
    Categories = ListField(StringField(required=True), required=False, default=[])
    Views = IntField(min_value=0, default=0)
    Likes = IntField(min_value=0, default=0)
    FeaturedImageUrl = StringField(required=False, default=None)
```

to ensure the security, we need to insert permission settings to `EntityDefaultPermissionSettings`. 


```json
{
    "_id" : "7da1cebe-5c04-47bd-a3df-d60b6dfe45cf", 
    "EntityName" : "BlogPost", 
    "IdsAllowedToRead" : ["owner"], 
    "IdsAllowedToWrite" : [], 
    "IdsAllowedToUpdate" : ["owner"], 
    "IdsAllowedToDelete" : ["owner"], 
    "RolesAllowedToWrite" : ["admin", "author"],
    "RolesAllowedToRead" : ["admin", "author", "anonymous", "editor", "user"], 
    "RolesAllowedToUpdate" : ["editor"], 
    "RolesAllowedToDelete" : []
}
```

Generic Rest Insert API implementation:

```python
from uuid import uuid4

from rest_framework import status
from rest_framework.response import Response

from django_pds.core.pds.generic import data_insert
from django_pds.core.rest.response import error_response, success_response
from django_pds.core.rest.views import BaseAPIView
from django_pds.core.rest.decorators import required


class GenericRestInsert(BaseAPIView):

    @required("document_name", "data")
    def post(self, request):
        try:
            
            document_name = request.data['document_name']
            data = request.data['data']

            # extract user id from jwt token
            # or from the request session or cookie
            # here user_id is required to
            # ensure row level security
            # added manually for testing purpose
            user_id = 'b3dfe7dd-1b88-49fd-a422-aa094ddd747b'
            
            error, result = data_insert(document_name, data, user_id)
            
            if error:
                response = error_response(result)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            response = success_response(result)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        except BaseException as e:
            response = error_response(str(e))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
```

So now and on, you don't have to create insert rest api for every single individual collection or document.

**`data_insert` method params:**

- `document_name`: Document name
- `data`: Collection data
- `force_insert`, default = False, When force_insert is True, data with same ItemId will be forced to replace the exiting data with the same ItemId
- `ignore_security`, default=False, when ignore_security is True, row level security checking will be disabled at the time of insertion. All the row level security fields will have an empty array 

**Data insertion without row level security:**

```python
......
......
class GenericRestInsert(BaseAPIView):

    @required("document_name", "data")
    def post(self, request):
        try:
            .....
            .....
            error, result = data_insert(document_name, data, ignore_security=True)
            .....
            
        except BaseException as e:
            response = error_response(str(e))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
```

**Data insertion without row level security isn't recommended but if you want to control security checking manually, you may set `ignore_security` to True** 