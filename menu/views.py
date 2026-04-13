

# Create your views here.

from django.shortcuts import render, get_object_or_404
from menu.models import Category, Product


def menu(request):
    categories= Category.objects.filter(is_active=True)
    products= Product.objects.filter(is_active=True)
    featured= Product.objects.filter(is_active=True, is_featured=True)

    context= {
        'categories': categories,
        'products': products,
        'featured': featured,}
    return render(request, 'menu/menu.html', context)


def product_detail(request, product_id):
    product= get_object_or_404(Product, id=product_id, is_active=True)
    product_options= product.productoption_set.select_related('option').all()

    option_groups= {}
    for po in product_options:
        group= po.option
        if group not in option_groups:
            option_groups[group]= group.options.filter(is_active=True)

    context= {
        'product': product,
        'option_groups': option_groups,}
    return render(request, 'menu/product_detail.html', context)