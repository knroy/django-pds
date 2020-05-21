# 1. Tutorial

This tutorial introduces **`django_pds`** by means of example. We will walk through how to create CRUD rest API for your website and by the term **`REST API`** we are actually referring a generic REST API, by which you can do all the CRUD operations without creating multiple endpoints for multiple MongoDB collections.

We will be creating a simple CRUD REST API with `django_pds`

### 1.1. Getting started

Before we start, make sure you have installed a MongoDB instance on your machine and running.

If you haven't installed `django_pds`, install it

```python
pip install django_pds
```

### 1.2. Defining our documents

`django_pds` has two pre-defined documents, `SimpleBaseDocument` and `BaseDocument`. In the later sections, we will be discussing how to use both of them.

As `django_pds` is built on top of `Django` and `MongoEngine`, we hope that you read their documentation as well.

### 1.2.1. Reason of two different base document

1. to be consistent with the use of generic `data_insert`, `data_update`, `data_delete` and `data_upsert` methods from `django_pds.core.pds.generic`
2. while defining a document, you must have to inherit either from `SimpleBaseDocument` or from `BaseDocument` from `django_pds.core.base` to use `data_insert`, `data_update`, `data_delete` and `data_upsert` methods from `django_pds.core.pds.generic`

### 1.2.2. BlogPost

let's define a document schema `BlogPost`:

```python
from mongoengine import StringField, ListField, IntField

from django_pds.core.base import BaseDocument


class BlogPost(BaseDocument):
    Title = StringField(max_length=500, required=True)
    Description = StringField(max_length=2000, required=True)
    Categories = ListField(StringField(required=True), required=False, default=[])
    Views = IntField(min_value=0, default=0)
    Likes = IntField(min_value=0, default=0)
    FeaturedImageUrl = StringField(required=False, default=None)
```

# 2. Insert Rest API

`django-pds` has two pre-defined document schema. `SimpleBaseDocument` and `BaseDocument`

`SimpleBaseDocument` contains only `ItemId` (an alias of `_id` of MongoDB index field) and doesn't contain [Row Level Security](https://github.com/knroy/django-pds/wiki/Row-Level-Security) fields and `BaseDocument` contains all the [Row Level Security](https://github.com/knroy/django-pds/wiki/Row-Level-Security) fields.

### 2.1. Data Insertion with `BaseDocument`

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

### 2.2. Generic Rest Insert API implementation:

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

### 2.2.1. `data_insert` method params

- `document_name`: Document name
- `data`: Collection data
- `force_insert`, default = False, When force_insert is True, data with same ItemId will be forced to replace the exiting data with the same ItemId
- `ignore_security`, default=False, when ignore_security is True, row level security checking will be disabled at the time of insertion. All the row level security fields will have an empty array 

### 2.2.2. Data insertion without row level security

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

# 3. Read Rest API

there are two different methods bundled in `django_pds` in `django_pds.core.pds.generic` module.
1. `basic_data_read`
2. `data_read`

### 3.1. Basic Data Read Rest API

Now we'll think about how to read data from the collections by document. As it turns out, `basic_read_data` method is a simple helper method for your generic read rest api where security isn't a concern. To start with `basic_read_data` method, we just need two things

1. Document Name, here we can use `BlogPost` or we can define a new Document Schema
2. Fields, a list or tuple or a string equals to `__all__`

### 3.1.1. `basic_data_read` example

`basic_data_read` method doesn't support Row Level Security. It's easiest but not recommended unless you check security manually before requesting for the data.

```python
from django_pds.core.rest.views import BaseAPIView
from django_pds.core.pds.generic import basic_data_read
from django_pds.core.rest.response import error_response

from rest_framework.response import Response
from rest_framework import status

class BasicDataReadRestAPI(BaseAPIView):

    def get(self, request):
        try:
            document_name = 'BlogPost'
            fields = ('ItemId', 'Title', 'Categories', 'Views', 'Likes', 'FeaturedImageUrl')
            error, data_or_exception = basic_data_read(document_name, fields=fields)
            return Response(data_or_exception, status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
```

`django_pds` has a generic document serializer so that you don't have to be worried about json data response. you can select fields without creating multiple document serializer.

still now `basic_data_read` method doesn't have filters, but have plans to implement filters in the upcoming versions

### 3.1.1.1. `basic_data_read` dynamic API
    
```python
from django_pds.core.rest.views import BaseAPIView
from django_pds.core.rest.decorators import required
from django_pds.core.pds.generic import basic_data_read
from django_pds.core.rest.response import error_response

from rest_framework.response import Response
from rest_framework import status


class BasicDataReadRestAPI(BaseAPIView):

    required("document_name", "fields")
    def post(self, request):

        try:

            document_name = request.data['document_name']
            fields = request.data['fields']
            page_size = request.data.get('pageSize', 10)  # optional params
            page_number = request.data.get('pageNumber', 1)  # optional params
            order_by = request.data.get('order_by', [])  # optional params
            error, data_or_exception = basic_data_read(document_name, fields=fields, 
                                                       page_size=page_size, page_num=page_number, 
                                                       order_by=order_by)
            return Response(data_or_exception, 
                            status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)

        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
```

### 3.2. `read_data` method

to develop a [row level secured](https://github.com/knroy/django-pds/wiki/Row-Level-Security) read endpoint, you have to use `read_data` method from `django_pds.core.pds.generic` module

###  3.2.1. Generic Read EndPoint Implementation

as we defined [`BlogPost`](#122-blogpost) document earlier, and inserted [row level security permission](#21-data-insertion-with-basedocument) where we allowed users with roles `"admin", "author", "anonymous", "editor", "user"` can read the document, as a result, a `BlogPost` document can be read by a user who has one of these roles.

before we start implementing the Row Level Secured Read REST API endpoint, let's get us introduced a specific SQL like query string, which will be used to read data using the endpoint.

check this following query:

```
Select<Item,Likes,Views,Title> From<BlogPost> Where<Likes=20>
```

This query will be sent to the rest API, where the string will be processed using a parser and will be transforming into a `MongoEngine` query filter.

The main focus of the `read_data` method is to reduce backend development time and cost. Once this endpoint is implemented, you don't have to change it for different types of document you define. You just implement the read endpoint once and define as many documents as you want and rest of the queries will be coming from frontend.

So, by this query, we want to select  `Item,Likes,Views,Title` from `BlogPost` Document where a document contains `20` likes.

Now, how to query a `BlogPost` information?

We have inserted two different document in `BlogPost`.

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
    "RolesAllowedToWrite" : [], 
    "RolesAllowedToRead" : ["admin", "author", "anonymous", "editor", "user"], 
    "RolesAllowedToUpdate" : ["editor"],
    "RolesAllowedToDelete" : [], 
    "Title" : "django-pds :: Faster REST API development with Djagno and MongoDB", 
    "Description" : "This tutorial introduces django_pds by means of example. We will walk through how to create CRUD rest API for your website and by the term REST API we are actually referring a generic REST API, by which you can do all the CRUD operations without creating multiple endpoints for multiple MongoDB collections.", 
    "Categories" : ["django_pds", "mongoengine", "mongodb"],
    "Views" : 950,
    "Likes" : 21,
    "FeaturedImageUrl" : "https://images.unsplash.com/photo-1589129983227-8fea3db1e07f"
}
```

```json
{ 
    "_id" : "e97534c6-fe3f-449c-a3b3-b64ea63385e7", 
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
    "RolesAllowedToWrite" : [], 
    "RolesAllowedToRead" : ["admin", "author", "anonymous", "editor", "user"], 
    "RolesAllowedToUpdate" : ["editor"],
    "RolesAllowedToDelete" : [], 
    "Title" : "Django REST Framework", 
    "Description" : "If we're still need a few more percentage points of performance, we can simply return a regular HttpResponse from our views, rather than returning a REST framework Response. That'll give us some very minor time savings as the full response rendering process won't need to run. The standard JSON renderer also uses a custom encoder that properly handles various cases such as datetime formatting, which in this case we don't need.",
    "Categories" : ["django", "rest_framework"],
    "Views" : 1000,
    "Likes" : 12,
    "FeaturedImageUrl" : "https://images.unsplash.com/photo-1589900274474-80331313d098"
}
```

basically we need two things in the payload for the generic REST API to read data from server.

1. Document Name
2. query string (very similar with MySQL query)

our payload should look like below json object:

```json
{
    "document_name": "BlogPost",
    "query": "SELECT<ItemId,Likes,Views,Title> FROM<BlogPost> OrderBy<Title> PageSize<10> PageNumber<1>"
}
```

by using generic data read method, all you need is to implement the REST API View. Here is an example of read REST API View.

```python
from rest_framework import status
from rest_framework.response import Response

from django_pds.core.pds.generic import data_read
from django_pds.core.rest.decorators import required
from django_pds.core.rest.response import error_response, success_response
from django_pds.core.rest.views import BaseAPIView


class GenericReadRestAPI(BaseAPIView):

    required("document_name", "query")
    def post(self, request):

        try:
            params = request.data

            document_name = params['document_name']
            query = params['query']
            
            # here the below user id is manually added
            # for demonstration purpose
            # you can extract an user id from the request
            # or from the jwt token if you implement
            user_id = '862bdaf0-6fa4-476e-be07-43ededfc222c'

            error, data = data_read(document_name, query, user_id=user_id)

            return Response(data, status=status.HTTP_200_OK if not error else status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            return Response(error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
```

**Query - 1**

```json
{
    "document_name": "BlogPost",
    "query": "SELECT<ItemId,Likes,Views,Title> FROM<BlogPost> Where<Likes__gte=20> OrderBy<Title> PageSize<10> PageNumber<1>"
}
```

**`Likes__gte` is basically Likes is greater-than or equal**

Response:

```json
{
    "success_status": 200,
    "error": null,
    "success_description": "request valid",
    "results": [
        {
            "ItemId": "2e9fa69f-7180-4ddc-b25e-17fedb9872ab",
            "Likes": 21,
            "Views": 950,
            "Title": "django-pds :: Faster REST API development with Djagno and MongoDB"
        }
    ],
    "total_records": 1
}
```

**Query - 2**

```json
{
    "document_name": "BlogPost",
    "query": "SELECT<ItemId,Likes,Views,Title> FROM<BlogPost> Where<Likes__lte=10> OrderBy<Title> PageSize<10> PageNumber<1>"
}
```

**`Likes__lte` is basically age is less-than or equal**

Response:

```json
{
    "success_status": 200,
    "error": null,
    "success_description": "request valid",
    "results": [],
    "total_records": 0
}
```

**Query - 3 :: Conditional Where Clause**

```json
{
    "document_name": "BlogPost",
    "query": "SELECT<ItemId,Title, Description> FROM<BlogPost> Where<Likes__gte=20 & (Title__icontains=django | Description__icontains=django)> OrderBy<Title> PageSize<10> PageNumber<1>"
}
```

**`Likes__gte` is basically Likes is greater-than or equal**

Response:

```json
{
    "success_status": 200,
    "error": null,
    "success_description": "request valid",
    "results": [
        {
            "ItemId": "2e9fa69f-7180-4ddc-b25e-17fedb9872ab",
            "Title": "django-pds :: Faster REST API development with Djagno and MongoDB",
            "Description": "This tutorial introduces django_pds by means of example. We will walk through how to create CRUD rest API for your website and by the term REST API we are actually referring a generic REST API, by which you can do all the CRUD operations without creating multiple endpoints for multiple MongoDB collections."
        }
    ],
    "total_records": 1
}
```

Read `MongoEngine` documentation to find out more about [Query Operators](http://docs.mongoengine.org/guide/querying.html#query-operators)

**Our Query String parser deos support the following Query Operators in a different way:**

`geo_within_center`

`geo_within_sphere`

`within_spherical_distance`

`within_box`

`within_polygon`

You have to send them as json object array. not as point.
Example:

Wrong Way: 

```json
{
    "document_name": "Location",
    "query": "SELECT<ItemId,Lat, Long> FROM<Location> Where<point__geo_within_sphere=[(-125.0, 35.0), 1]>"
}
```

Right Way: 

```json
{
    "document_name": "Location",
    "query": "SELECT<ItemId,Lat, Long> FROM<Location> Where<point__geo_within_sphere=[[-125.0, 35.0], 1]>"
}
```