from django.conf.urls import url
from django.urls import path
from payment import views

app_name = 'payment'

urlpatterns = [
    path('', views.list_payments, name='list_payment'),
    path('checkout/<uuid:pk>/', views.checkout, name='checkout'),
    path('<uuid:pk>/', views.payment_detail, name='payment-detail'),
    # url(r'^save-stripe-info/$', views.save_stripe_info, name='save-stripe-info'),
]