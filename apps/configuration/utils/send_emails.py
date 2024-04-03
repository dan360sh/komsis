from apps.configuration.models.settings import Settings
from apps.feedback.models.email import Email
from apps.feedback.utils import template_email_message
from apps.shop.models import Order
from django.http import HttpRequest


def send_order_emails(order: Order, request: HttpRequest):
    web_settings = Settings.objects.first()
    template_email_message(
        'shop/order-mail.html', subject="Ваш заказ №" + str(order.id),
        to=[order.email], data={
            'order': order, 'request': request,
            'color': web_settings.color_scheme})
    res = [item.title for item in Email.objects.all()]

    template_email_message(
        'shop/order-mail.html',
        subject="Новый заказ №" + str(order.id), to=res, data={
            'order': order, 'request': request,
            'color': web_settings.color_scheme})
    if order.account.manager is not None:
        template_email_message(
            'shop/order-mail.html',
            subject="Новый заказ №" + str(order.id), to=[order.account.manager.email],
            data={
                'order': order, 'request': request,
                'color': web_settings.color_scheme
            }
        )
