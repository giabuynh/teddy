from django.urls import path
from order.views import OrderView, OrderDetailView

app_name = 'order'

urlpatterns = [
    path('', OrderView.as_view(), name='order-list'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
]