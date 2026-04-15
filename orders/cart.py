from decimal import Decimal
from menu.models import Product, Option


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})
        if self.SESSION_KEY not in self.session:
            self.session[self.SESSION_KEY] = self.cart

    def _build_key(self, product_id, option_ids):
        normalized = sorted(str(option_id) for option_id in option_ids)
        suffix = "-".join(normalized)
        return f"{product_id}:{suffix}"

    def add(self, product_id, quantity=1, option_ids=None):
        option_ids = option_ids or []
        key = self._build_key(product_id, option_ids)

        if key in self.cart:
            self.cart[key]["quantity"] += quantity
        else:
            self.cart[key] = {
                "product_id": product_id,
                "quantity": quantity,
                "option_ids": sorted(option_ids),
            }

        self.save()

    def update(self, item_key, quantity):
        if item_key in self.cart:
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

            options = list(Option.objects.filter(id__in=item["option_ids"], is_active=True))
            option_total = sum((option.extra_price for option in options), Decimal("0.00"))
            unit_price = product.price + option_total
            line_total = unit_price * item["quantity"]
            grand_total += line_total

            items.append({
                "key": item_key,
                "product": product,
                "quantity": item["quantity"],
                "options": options,
                "unit_price": unit_price,
                "line_total": line_total,
            })

        return items, grand_total