from django.urls import path
from . import views

urlpatterns = [
    path('destinations/', views.destination_list, name='destination-list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
]
