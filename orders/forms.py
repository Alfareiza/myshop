from django import forms

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    """This form is reached at the moment of the checkout"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']