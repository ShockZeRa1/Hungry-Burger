from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from menu.models import Option
from orders.cart import Cart
from orders.models import DiscountCode, Order, OrderItem, OrderItemOption, OrderStatus


def calculate_discount(discount_code, cart_total):
    if discount_code.discount_type == "percentage":
        discount_amount = cart_total * (discount_code.value / Decimal("100"))
        return discount_amount.quantize(Decimal("0.01"))

    if discount_code.discount_type == "fixed":
        return min(discount_code.value, cart_total).quantize(Decimal("0.01"))

    return Decimal("0.00")


def validate_discount_code(code, cart_total):
    if not code:
        return None, Decimal("0.00"), "Please enter a discount code."

    try:
        discount_code = DiscountCode.objects.get(code__iexact=code.strip())
    except DiscountCode.DoesNotExist:
        return None, Decimal("0.00"), "Invalid discount code."

    if not discount_code.is_active:
        return None, Decimal("0.00"), "This discount code is not active."

    if discount_code.valid_until and discount_code.valid_until < timezone.now():
        return None, Decimal("0.00"), "This discount code has expired."

    if discount_code.max_uses is not None and discount_code.used_count >= discount_code.max_uses:
        return None, Decimal("0.00"), "This discount code has already been fully used."

    if cart_total < discount_code.min_order_amount:
        return None, Decimal("0.00"), f"Minimum order amount for this code is kr {discount_code.min_order_amount}."

    discount_amount = calculate_discount(discount_code, cart_total)
    return discount_code, discount_amount, None


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


def apply_discount_view(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request."}, status=400)

    cart = Cart(request)
    cart_items, grand_total = cart.get_items()

    if not cart_items:
        return JsonResponse({"success": False, "message": "Your cart is empty."}, status=400)

    code = request.POST.get("discount_code", "").strip()
    discount_code, discount_amount, error = validate_discount_code(code, grand_total)

    if error:
        request.session.pop("active_discount_code", None)
        request.session.modified = True

        return JsonResponse({
            "success": False,
            "message": error,
            "subtotal": str(grand_total),
            "discount_amount": "0.00",
            "final_total": str(grand_total),
        })

    final_total = grand_total - discount_amount

    request.session["active_discount_code"] = discount_code.code
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": f"Discount code {discount_code.code} activated.",
        "subtotal": str(grand_total),
        "discount_amount": str(discount_amount),
        "final_total": str(final_total.quantize(Decimal("0.01"))),
    })


def checkout_view(request):
    cart = Cart(request)
    cart_items, grand_total = cart.get_items()

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect("menu")

    discount_code_input = request.session.get("active_discount_code", "")
    discount_code = None
    discount_amount = Decimal("0.00")
    final_total = grand_total

    if discount_code_input:
        discount_code, discount_amount, discount_error = validate_discount_code(
            discount_code_input,
            grand_total,
        )

        if discount_error:
            request.session.pop("active_discount_code", None)
            request.session.modified = True
            discount_code_input = ""
            discount_amount = Decimal("0.00")
            final_total = grand_total
        else:
            final_total = grand_total - discount_amount

    if request.method == "POST":
        customer_note = request.POST.get("customer_note", "").strip()
        guest_name = request.POST.get("guest_name", "").strip()
        guest_email = request.POST.get("guest_email", "").strip()
        discount_code_input = request.POST.get("discount_code", "").strip()

        if discount_code_input:
            discount_code, discount_amount, discount_error = validate_discount_code(
                discount_code_input,
                grand_total,
            )
            
            if discount_error:
                messages.error(request, discount_error)
                return redirect("checkout")
            final_total = grand_total - discount_amount

        if not request.user.is_authenticated:
            if not guest_name or not guest_email:
                messages.error(request, "Please enter your name and email to place a guest order.")
                return redirect("checkout")

        status, _ = OrderStatus.objects.get_or_create(
            name="Order Placed",
            defaults={"is_active": True},
        )

        order = Order.objects.create(
            order_type="pickup",
            total_amount=final_total,
            customer=request.user if request.user.is_authenticated else None,
            guest_name=guest_name if not request.user.is_authenticated else "",
            guest_email=guest_email if not request.user.is_authenticated else "",
            status=status,
            customer_note=customer_note,
            discount_code=discount_code,
            discount_amount=discount_amount,
        )

        if discount_code:
            discount_code.used_count += 1
            discount_code.save()

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

        request.session.pop("active_discount_code", None)
        cart.clear()

        messages.success(request, f"Order #{order.id} placed successfully.")
        return redirect("menu")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "grand_total": grand_total,
        "discount_code_input": discount_code_input,
        "discount_amount": discount_amount,
        "final_total": final_total,
    })


@login_required
def past_orders_view(request):  
    orders = (
        Order.objects.filter(customer=request.user)
        .prefetch_related("orderitem_set__orderitemoption_set")
        .select_related("status", "discount_code")
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