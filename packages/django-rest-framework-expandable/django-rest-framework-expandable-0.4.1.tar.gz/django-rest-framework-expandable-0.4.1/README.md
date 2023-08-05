# Django Rest Framework Expandable

## Description

Expandable serializers for Django REST Framework. Allow for selective object
expansion through query parameters or serializer class kwargs.

## Installation

```
pip install django-rest-framework-expandable
```

## Usage

```python
# apps/users/api.serializers.py
# (User serializer)
class UserSerializer(ExpandableHyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ("username", "id", ...)

# apps/users/api/fields.py
# (User expandable serializer field)
class UserRelatedField(ExpandableHyperlinkedRelatedField):
  queryset = User.objects.all()
  lookup_field = "id"
  view_name = "api:user-detail"
  expand_settings = {
    "comparison_fields": ["id"],
    "serializers": [
      {
        "paths": ["example.user"],
        "serializer": "apps.users.api.serializers.UserSerializer",
        "skipped": [],
      }
    ]
  }

# apps/example/api/serializers.py
# Example serializer (using nested expandable serializer fields)
from apps.users.api.fields import UserRelatedField
from apps.another.api.fields import AnotherRelatedField

class ExampleSerializer(ExpandableHyperlinkedModelSerializer):
  another_related_field = AnotherRelatedField()
  user = UserRelatedField()
  ...
```

Returns...

```
GET http://localhost:8000/api/examples/?expand=example.user
{
  id: 1,
  another_related_field: "http://localhost:8000/api/another/1",
  user: {
    id: 1,
    username: "Alex",
    ...
  }
}
```
