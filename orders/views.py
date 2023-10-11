from django.shortcuts import render

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


def order_create(request):
    """
    The current cart is obtained from the session
    In case of GET:
        - Instance the form and render the template
    In case of POST:
        - Validate the data which comes in the request.
        - Create an Order in the DB using form.save()
        - Create a OrderItem for every item in the cart.
        - Clean the cart.
        - Render the template.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # Clean the cart
                cart.clear()
                return render(request,
                              'orders/order/created.html',
                              {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

