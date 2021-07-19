from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import CustomUserCreate, BlackListTokenUpdateView

app_name = 'authentication'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name='create_user'),
    path('logout/', BlackListTokenUpdateView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
]