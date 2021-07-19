from django.conf.urls import url

from pay import views

app_name = 'pay'

urlpatterns = [
    url(r'^test-payment/$', views.test_payment),
    url(r'^save-stripe-info/$', views.save_stripe_info)
]