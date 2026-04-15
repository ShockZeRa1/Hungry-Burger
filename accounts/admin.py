from django.contrib import admin

from .models import Order, OrderItem, OrderItemOption, OrderStatus

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount')
    list_filter = ('status', 'created_at') # Adds a sidebar to filter by "Preparing Order", "Ready", etc.

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderItemOption)
admin.site.register(OrderStatus)