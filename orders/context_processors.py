from decimal import Decimal
from orders.cart import cart_summary


def floating_cart(request):
    try:
        summary = cart_summary(request)
    except Exception:
        summary = {
            "items": [],
            "total_quantity": 0,
            "grand_total": Decimal("0.00"),
            "is_empty": True,
        }

    return {
        "floating_cart": summary
    }