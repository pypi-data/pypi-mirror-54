# Constants-set
- Simple constants sets for Python.
- Kind of like enums, reusable constants.
- Kind of convenient for Django and DRF.

## Use cases

### Simple python
```python
from constants_set import ConstantsSet


class Book:
    TYPES = ConstantsSet(["ROMANCE", "ACTION"])

    def __init__(self, type):
        self.type = type

    def get_global_feeling(self):
        if self.type == Book.TYPES.ROMANCE:
            return 'love'
        if self.type == Book.TYPES.ACTION:
            return 'intensity'
```


### Django model
```python
from django.db import models


class BookModel(models.Model):
    type = models.CharField(max_length=30, choices=Book.TYPES.to_choices(), default=Book.TYPES.ROMANCE)
```


### Django rest framework serializer
```python
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=Book.TYPES.to_choices())
```
