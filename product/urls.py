from django.urls import path
from product.views import ProductView, ProductDetailView, ImageView, ImageDetailView, ProductSizeView, \
    ProductSizeDetailView

app_name = 'product'

urlpatterns = [
    path('', ProductView.as_view(), name='product-list'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('image/', ImageView.as_view(), name='image-list'),
    path('image/<uuid:url>', ImageDetailView.as_view(), name='image-detail'),
    path('size/', ProductSizeView.as_view(), name='product-size-list'),
    path('size/<uuid:url>', ProductSizeDetailView.as_view(), name='product-size-detail'),
]