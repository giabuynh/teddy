from rest_framework import serializers
from product.models import Product, Image, ProductSize


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'imageURLs']
        read_only_fields = ['id']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['id', 'product', 'size', 'quantity', 'price', 'stripe_id']
        read_only_fields = ['id']