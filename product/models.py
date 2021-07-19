import uuid
from django.db import models
from category.models import Category


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.url


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(max_length=1000)
    imageURLs = models.ManyToManyField(Image)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    stripe_id = models.CharField(max_length=200, blank=False)

    class Meta:
        unique_together = (('product', 'size'),)

    def __str__(self):
        return self.product.name + " " + self.size
