from django.urls import path
from menu import views

urlpatterns= [path('', views.menu, name='menu'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),]
