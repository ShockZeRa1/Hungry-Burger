from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from menu.forms import CustomisationForm
from menu.models import Category, Product
from orders.cart import Cart


def menu(request):
    categories = Category.objects.filter(is_active=True).order_by("sort_order")
    products = Product.objects.filter(is_active=True)
    featured = Product.objects.filter(is_active=True, is_featured=True)

    context = {
        "categories": categories,
        "products": products,
        "featured": featured,
    }
    return render(request, "menu/menu.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    product_options = product.productoption_set.select_related("option").all()

    option_groups = {}
    for po in product_options:
        group = po.option
        if group not in option_groups:
            option_groups[group] = group.option_set.filter(is_active=True)

    if request.method == "POST":
        form = CustomisationForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            selected_options = []
            for key, val in request.POST.items():
                if key.startswith("option_"):
                    selected_options.append(int(val))

            cart = Cart(request)
            cart.add(
                product_id=product.id,
                quantity=quantity,
                option_ids=selected_options,
            )

            messages.success(request, f"{product.name} added to cart.")
            return redirect("cart")
    else:
        form = CustomisationForm()

    context = {
        "product": product,
        "option_groups": option_groups,
        "form": form,
    }
    return render(request, "menu/product_detail.html", context)