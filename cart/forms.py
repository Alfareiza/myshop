from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # Allow to the user choose a quantity between 1 and 20
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int  # Transform the input to int
    )
    # Allor to know if the quantity must add up or not
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
