from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from coupons.models import Coupon


@require_POST
def coupon_apply(request):
    """Checks the coupon and store it in the session it is ok"""
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExit:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')