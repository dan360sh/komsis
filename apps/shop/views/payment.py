from apps.configuration.utils import BankPayment
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from ..models import Order


class PaymentRedirectView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'account-orders'

    def get_redirect_url(self, *args, **kwargs):
        order = get_object_or_404(
            Order, bank_id=self.request.GET.get("orderId", "None"))
        payment = BankPayment(order, self.request)

        if payment.is_valid():
            payment.set_status_order()

        if not self.request.user.is_authenticated:
            self.url = "/"

        return super().get_redirect_url(*args, **kwargs)
