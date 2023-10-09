from cart.cart import Cart


def cart(request):
    # Now, the cart instance is available in all templates.
    return {'cart': Cart(request)}
