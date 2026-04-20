from decimal import Decimal

from menu.models import Option, Product


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.SESSION_KEY)

        if not cart:
            cart = {}
            self.session[self.SESSION_KEY] = cart

        self.cart = cart

    def _build_key(self, product_id, option_ids):
        normalized_option_ids = sorted(str(option_id) for option_id in option_ids)
        suffix = "-".join(normalized_option_ids)
        return f"{product_id}:{suffix}"

    def add(self, product_id, quantity=1, option_ids=None):
        option_ids = option_ids or []
        item_key = self._build_key(product_id, option_ids)

        if item_key in self.cart:
            self.cart[item_key]["quantity"] += int(quantity)
        else:
            self.cart[item_key] = {
                "product_id": int(product_id),
                "quantity": int(quantity),
                "option_ids": [int(option_id) for option_id in option_ids],
            }

        self.save()

    def update(self, item_key, quantity):
        if item_key in self.cart:
            quantity = int(quantity)

            if quantity > 0:
                self.cart[item_key]["quantity"] = quantity
            else:
                del self.cart[item_key]

            self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.cart = self.session[self.SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True

    def count(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_items(self):
        items = []
        grand_total = Decimal("0.00")

        for item_key, item in self.cart.items():
            try:
                product = Product.objects.get(id=item["product_id"], is_active=True)
            except Product.DoesNotExist:
                continue

            option_ids = item.get("option_ids", [])
            options = list(Option.objects.filter(id__in=option_ids, is_active=True))

            options_total = sum((option.extra_price for option in options), Decimal("0.00"))
            unit_price = product.price + options_total
            quantity = int(item["quantity"])
            line_total = unit_price * quantity

            grand_total += line_total

            items.append({
                "key": item_key,
                "product": product,
                "quantity": quantity,
                "options": options,
                "unit_price": unit_price,
                "line_total": line_total,
            })

        return items, grand_total


def cart_summary(request):
    cart = Cart(request)
    items, grand_total = cart.get_items()

    total_quantity = sum(item["quantity"] for item in items)

    return {
        "items": items,
        "total_quantity": total_quantity,
        "grand_total": grand_total,
        "is_empty": len(items) == 0,
    }