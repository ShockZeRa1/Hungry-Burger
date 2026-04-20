from django.urls import path
from orders import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/update/<str:item_key>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<str:item_key>/", views.remove_cart_item, name="remove_cart_item"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("past-orders/", views.past_orders_view, name="past_orders"),
    path("reorder/<int:order_id>/", views.reorder_view, name="reorder"),
]