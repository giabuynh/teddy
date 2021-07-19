import json
import uuid

import stripe
from django.http import QueryDict
from django.shortcuts import render
from rest_framework import mixins, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product, ProductSize, Image
from product.serializers import ProductSerializer, ProductSizeSerializer, ImageSerializer


class ImageView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.create(request, *args, **kwargs)


class ImageDetailView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.destroy(request, *args, **kwargs)


class ProductView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.create(request, *args, **kwargs)


class ProductDetailView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.destroy(request, *args, **kwargs)


class ProductSizeView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser and request.user.is_active):
            return
        data = request.data.copy()
        product = stripe.Product.create(
            name=Product.objects.get(id=data['product']).name + ' ' + data['size'],
            type="good",
        )
        stripe.Price.create(
            product=product.id,
            unit_amount=data['price'],
            currency='vnd',
        )
        stripe.SKU.create(
            price=data['price'], #temp - should init cost of product
            currency='vnd',
            inventory={'type': 'finite', 'quantity': data['quantity']},
            product=product.id,
        )
        request.POST._mutable = True
        request.data['stripe_id'] = product.id
        return self.create(request, *args, **kwargs)


class ProductSizeDetailView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.destroy(request, *args, **kwargs)