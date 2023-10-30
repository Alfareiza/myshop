from django import forms
from localflavor.us.forms import USZipCodeField

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    """This form is reached at the moment of the checkout and
    it is a model form, it's based on fields of a model."""
    # This field which comes from the lib django-localflavor
    # will overwrite the field originally of the user.
    postal_code = USZipCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']