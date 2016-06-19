# -*- coding: utf-8 -*-
from django.core.mail import send_mail
def default_payment_handler(request, order_form, order):
    """
    Default payment handler - called when the final step of the
    checkout process with payment information is submitted. Implement
    your own and specify the path to import it from via the setting
    ``SHOP_HANDLER_PAYMENT``. This function will typically contain
    integration with a payment gateway. Raise
    cartridge.shop.checkout.CheckoutError("error message") if payment
    is unsuccessful.
    """
    send_mail(
        u"Ծախվե՜՜՜ց",
        u"Գոհարի՜՜՜՜՜՜՜՜՜՜կ, արագ մտի նայի, ծախվելա ծախվել։",
        'info@cart4brand.com',
        ['davsmile@yahoo.com'],
        fail_silently=True,
    )
