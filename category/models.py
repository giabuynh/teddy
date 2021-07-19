import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
