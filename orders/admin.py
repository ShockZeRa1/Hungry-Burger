from django.contrib import admin
from orders.models import DiscountCode, Order, OrderItem, OrderItemOption, OrderStatus


class OrderItemOptionInline(admin.TabularInline):
    model = OrderItemOption
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "value",
        "min_order_amount",
        "max_uses",
        "used_count",
        "valid_until",
        "is_active",
    )
    list_filter = ("discount_type", "is_active", "valid_until")
    search_fields = ("code",)


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "guest_name",
        "guest_email",
        "order_type",
        "total_amount",
        "discount_code",
        "discount_amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at", "order_type")
    search_fields = ("customer__username", "guest_name", "guest_email")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name_snapshot", "quantity", "unit_price_snapshot")
    inlines = [OrderItemOptionInline]


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_item", "option_name_snapshot", "extra_price_snapshot")