
# Register your models here.

from django.contrib import admin
from menu.models import Category, Product, ProductOption, Option, OptionGroup


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
    list_display= ('name', 'category', 'price', 'is_featured', 'is_active')
    list_filter= ('category', 'is_featured', 'is_active')
    search_fields= ('name',)
    ordering= ('-is_featured', 'name')
    inlines= [ProductOptionInline]


admin.site.register(Product, ProductAdmin)
