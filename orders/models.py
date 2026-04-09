from django.db import models
from django.contrib.auth.models import User


# Tracks where the food is (e,g, "Order placed", "Being prepared" or "Ready")
class OrderStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Order Statuses"

    def __str__(self):
        return self.name


# Acts as a receipt for all the information about the order and the person who ordered it
class Order(models.Model):
    order_type = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)

    def __str__(self):
        return f"Order {self.id} - {self.customer}"
    

# The specific item inside the order
from menu.models import Product
class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # These snapshots store the old price of an item and lock the price so that new prices of the exacr item will not affect it.
    product_name_snapshot = models.CharField(max_length=255)
    unit_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name_snapshot}"
    

# Customization of a specific order is tracked for that one order (e.g. "The chicken burger had extra lettuce")
class OrderItemOption(models.Model):
    option_name_snapshot = models.CharField(max_length=255)
    extra_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Option: {self.option_name_snapshot}"