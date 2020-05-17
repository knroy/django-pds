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

there are two different methods bundled in `django_pds` in `django_pds.core.pds.generic` module.
1. `basic_data_read`
2. `data_read`
 