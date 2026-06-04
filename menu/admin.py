from django.contrib import admin
from django.db.models import Sum
from menu.models import Category, Product, ProductOption, Option, OptionGroup
from orders.models import OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display= ('name', 'sort_order', 'is_active')
    list_filter= ('is_active',)
    search_fields= ('name',)
    ordering= ('sort_order',)


admin.site.register(Category, CategoryAdmin)


class OptionGroupAdmin(admin.ModelAdmin):
    list_display= ('name', 'selection_type', 'is_active')
    list_filter= ('is_active',)
    search_fields= ('name',)


admin.site.register(OptionGroup, OptionGroupAdmin)


class OptionAdmin(admin.ModelAdmin):
    list_display= ('name', 'option_group', 'extra_price', 'is_active')
    list_filter= ('option_group', 'is_active')
    search_fields= ('name',)


admin.site.register(Option, OptionAdmin)


class ProductOptionInline(admin.TabularInline):
    # shows option groups directly inside the product page
    model= ProductOption
    extra= 1


class ProductAdmin(admin.ModelAdmin):
    list_display= ('name', 'category', 'price', 'is_featured', 'is_active', 'units_sold', 'revenue')
    list_filter= ('category', 'is_featured', 'is_active')
    search_fields= ('name',)
    ordering= ('-is_featured', 'name')
    inlines= [ProductOptionInline]

    def units_sold(self, obj):
        result = OrderItem.objects.filter(product=obj).aggregate(total=Sum('quantity'))
        return result['total'] or 0
    units_sold.shirt_description = 'Units sold'

    def revenue(self, obj):
        items = OrderItem.objects.filter(product=obj)
        total = 0
        for item in items:
            total += item.quantity * item.unit_price_snapshot
        return f"{total:.2f}"
    revenue.short_description = 'Revenue'


admin.site.register(Product, ProductAdmin)
