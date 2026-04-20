from django.contrib import admin
from orders.models import Order, OrderItem, OrderItemOption, OrderStatus


class OrderItemOptionInline(admin.TabularInline):
    model = OrderItemOption
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "order_type", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at", "order_type")
    search_fields = ("customer__username",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name_snapshot", "quantity", "unit_price_snapshot")
    inlines = [OrderItemOptionInline]


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_item", "option_name_snapshot", "extra_price_snapshot")