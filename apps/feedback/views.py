from apps.catalog.models import Product
from django.http import JsonResponse
from django.views import View

from .models import Email, Subscriber
from .utils import template_email_message


class SubscribeView(View):

    def post(self, request, *args, **kwargs):
        error_list = {}
        fields = request.POST

        if fields['email'] == '':
            error_list['email'] = 'Укажите email'

        if not error_list:
            subscriber = Subscriber.objects.update_or_create(
                email=fields['email'], defaults=({'email': fields['email']}))

            # Проверка подписан человек или нет
            if subscriber[1]:
                res = [item.title for item in Email.objects.all()]
                template_email_message(
                    'feedback/send-mail/subscribe.html',
                    subject=fields['subject'], to=res, data=fields)
                return JsonResponse({
                    'errors': False,
                    'message': 'Подписка оформлена'
                })
            else:
                return JsonResponse({
                    'errors': False,
                    'message': 'Вы уже подписаны'
                })
        else:
            return JsonResponse({'errors': True, 'fields': error_list})


class QuestionView(View):

    def post(self, request, *args, **kwargs):
        error_list = {}
        fields = {}
        phone = request.POST.get('phone')
        phone_numbers = [v for v in phone if v.isdigit()]
        for k, v in request.POST.items():
            fields[k] = v
        # if fields['subject'] != 'Заявка на звонок':
        #     if fields['name'] == '':
        #         error_list['name'] = 'Укажите имя'
        if fields['phone'] == '' or len(phone_numbers) < 11:
            error_list['phone'] = 'Укажите телефон'
        # if fields['email'] == '':
        #     error_list['email'] = 'Укажите email'
        # if fields['message'] == '':
        #     error_list['message'] = 'Введите сообщение'
        if fields.get('product_id'):
            try:
                fields['product'] = Product.objects.get(pk=int(fields.get('product_id')))
            except:
                pass
        if not error_list:
            res = [item.title for item in Email.objects.all()]
            fields['site'] = "{}".format(request.get_host())
            template_email_message(
                'feedback/send-mail/question.html', subject=fields['subject'],
                to=res, data=fields)
            return JsonResponse({
                'errors': False,
                'message': 'Заявка успешно отправлена'
            })
        else:
            return JsonResponse({'errors': True, 'fields': error_list})


class ContactsFormView(View):

    def post(self, request, *args, **kwargs):
        error_list = {}
        fields = {}
        for k, v in request.POST.items():
            fields[k] = v
        fields['subject'] = 'Заявка на звонок'
        if fields['name'] == '':
            error_list['name'] = 'Укажите имя'
        if fields['phone'] == '':
            error_list['phone'] = 'Укажите телефон'
        if fields['email'] == '':
            error_list['email'] = 'Укажите email'
        if fields['message'] == '':
            error_list['message'] = 'Введите сообщение'
        if fields.get('product_id'):
            try:
                fields['product'] = Product.objects.get(pk=int(fields.get('product_id')))
            except:
                pass
        if not error_list:
            res = [item.title for item in Email.objects.all()]
            fields['site'] = "{}".format(request.get_host())
            template_email_message(
                'feedback/send-mail/question.html', subject=fields['subject'],
                to=res, data=fields)
            return JsonResponse({
                'errors': False,
                'message': 'Заявка успешно отправлена'
            })
        else:
            return JsonResponse({'errors': True, 'fields': error_list})


class OrderServiceView(View):

    def post(self, request, *args, **kwargs):
        error_list = {}
        fields = request.POST

        if fields['phone'] == '':
            error_list['phone'] = 'Укажите телефон'
        if fields['email'] == '':
            error_list['email'] = 'Укажите email'

        if not error_list:
            res = [item.title for item in Email.objects.all()]
            template_email_message(
                'feedback/send-mail/order-service.html',
                subject=fields['subject'], to=res, data=fields)
            return JsonResponse({
                'errors': False,
                'message': 'Заявка успешно отправлена'
            })
        else:
            return JsonResponse({'errors': True, 'fields': error_list})
