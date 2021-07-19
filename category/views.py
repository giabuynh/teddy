from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from category.models import Category
from category.serializers import CategorySerializer


class CategoryView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_active:
            return self.create(request, *args, **kwargs)


class CategoryDetailView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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
