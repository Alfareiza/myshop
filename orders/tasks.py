from io import BytesIO

import weasyprint
from celery import task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from orders.models import Order


@task
def order_created(order_id):
    """
    Task to send a notification by e-mail
    when an order is created successfully.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (f"Dear {order.first_name}, \n\n"
               f"You have successfully placed an order."
               f"Your order ID is {order.id}.")
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent


@task
def payment_completed(order_id):
    """
    Task to send a notification by email when an order is paid.
    This function is not being used in the project becayse the feature
    to pay wasn't implemented.
    However, It's important to notice how to handle with files if I'm
    planning to send them through e-mail
    """
    order = Order.objects.get(id=order_id)

    # Create the e-mail
    subject = f"My Shop - Invoice # {order.id}"
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    # Create the PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()  # BytesIO instance which is a buffer in memory
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    # Create the pdf having in count the BytesIO instance and add it the css style.
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach the file
    email.attach(f"order_{order.id}.pdf", out.getvalue(), 'application/pdf')

    # Send the e-mail
    email.send()
