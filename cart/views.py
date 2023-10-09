from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.models import Product


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update the cart.
    This view won't be accessible from urls instead of
    that only would be reached through POSTs.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    This view won't be accessible from urls instead of
    that only would be reached through POSTs.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')



def cart_detail(request):
    """
    Show the information of the cart.
    """
    cart = Cart(request)
    # Render multiple forms in one html, one per item in the cart
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request,
                  'cart/detail.html',
                  {'cart': cart})
