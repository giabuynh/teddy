from django.contrib import admin
from product.models import Product, Image, ProductSize

# Register your models here.
admin.site.register(Image)
admin.site.register(Product)
admin.site.register(ProductSize)
