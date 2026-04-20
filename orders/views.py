from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from menu.models import Option
from orders.cart import Cart
from orders.models import Order, OrderItem, OrderItemOption, OrderStatus


def cart_view(request):
    cart = Cart(request)
    cart_items, grand_total = cart.get_items()

    return render(request, "orders/cart.html", {
        "cart_items": cart_items,
        "grand_total": grand_total,
    })


def update_cart_item(request, item_key):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = Cart(request)
        cart.update(item_key, quantity)
        messages.success(request, "Cart updated successfully.")
    return redirect("cart")


def remove_cart_item(request, item_key):
    if request.method == "POST":
        cart = Cart(request)
        cart.remove(item_key)
        messages.success(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def checkout_view(request):
    cart = Cart(request)
    cart_items, grand_total = cart.get_items()

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect("menu")

    if request.method == "POST":
        status, _ = OrderStatus.objects.get_or_create(
            name="Order placed",
            defaults={"is_active": True},
        )

        order = Order.objects.create(
            order_type="pickup",
            total_amount=grand_total,
            customer=request.user,
            status=status,
        )

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                quantity=cart_item["quantity"],
                order=order,
                product=cart_item["product"],
                product_name_snapshot=cart_item["product"].name,
                unit_price_snapshot=cart_item["product"].price,
            )

            for option in cart_item["options"]:
                OrderItemOption.objects.create(
                    option_name_snapshot=option.name,
                    extra_price_snapshot=option.extra_price,
                    order_item=order_item,
                )

        cart.clear()
        messages.success(request, f"Order #{order.id} placed successfully.")
        return redirect("past_orders")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "grand_total": grand_total,
    })


@login_required
def past_orders_view(request):
    orders = (
        Order.objects.filter(customer=request.user)
        .prefetch_related("orderitem_set__orderitemoption_set")
        .select_related("status")
        .order_by("-created_at")
    )

    return render(request, "orders/past_orders.html", {
        "orders": orders,
    })


@login_required
def reorder_view(request, order_id):
    old_order = get_object_or_404(Order, id=order_id, customer=request.user)
    cart = Cart(request)

    for order_item in old_order.orderitem_set.prefetch_related("orderitemoption_set").all():
        if order_item.product is None:
            continue

        option_names = [
            option.option_name_snapshot
            for option in order_item.orderitemoption_set.all()
        ]

        option_ids = list(
            Option.objects.filter(name__in=option_names).values_list("id", flat=True)
        )

        cart.add(
            product_id=order_item.product.id,
            quantity=order_item.quantity,
            option_ids=option_ids,
        )

    messages.success(request, "Previous order added to cart.")
    return redirect("cart")