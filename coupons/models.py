from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):
    """
    This model is used to store the coupons
    """
    # Value which the user would put in the form
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()  # Since when is valid
    valid_to = models.DateTimeField()  # Until when is valid
    # How much will be applied (It's a percentage)
    # Acceptable 0 as minimum and 100 as maximum
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)]
    )
    active = models.BooleanField()  # Is active or not the coupon

    def __str__(self):
        return self.code
