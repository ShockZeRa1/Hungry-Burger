from django.urls import path, include

from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("orders/", views.past_orders, name="past_orders"),
    path("orders<id>/", views.order_detail, name="order_detail"),
]
