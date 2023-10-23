import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from .tasks import order_created
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


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
            order = form.save(commit=False)  # Is not still saved in db
            # If the cart has a coupon, then
            # save the coupon associated and his discount
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            # New object order is created
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # Clean the cart
                cart.clear()
                # Trigger an async task (Celery)
                # order_created.delay(order.id)
                return render(request,
                              'orders/order/created.html',
                              {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required  # Verify if is_active and is_staff are True
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',
                  {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response,  # Write the response into the weasyprint
                                           stylesheets=[weasyprint.CSS(  # Apply css to the generated pdf
                                               settings.STATIC_ROOT / 'css/pdf.css'
                                           )])
    return response
