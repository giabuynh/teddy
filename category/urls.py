from django.urls import path
from category import views

app_name = 'category'

urlpatterns = [
    path(r'', views.CategoryView.as_view(), name='category-list'),
    # path('', views.CreateCategory.as_view(), name='category-create'),
    path(r'<uuid:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    # path('<uuid:pk>/', views.DeleteCategory.as_view(), name='category-delete'),
]