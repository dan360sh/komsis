from datetime import datetime
from typing import Optional

import pdfkit
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, JsonResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import redirect as django_redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, View
from pyvirtualdisplay import Display

from apps.configuration.utils import Validator
from apps.feedback.models import Subscriber
from apps.google_captcha.decorators import check_recaptcha
from apps.shop.models import (Cart, Favorites, FavoritesItem, Order, OrderItem,
                              OrderState)

from .forms import ChangePasswordForm, LoginForm, RegisterForm
from .models import Account


# Представления на странцы пользователя личного кабинета
class OrdersList(LoginRequiredMixin, ListView):
    """Страница со списком заказаов в личном кабинете"""

    model = Order
    context_object_name = "orders"
    template_name = "account/orders.html"

    date_format = '%d.%m.%Y'
    current_page = 'natural_person'

    def post(self, request):
        qs = self.get_queryset()
        post_data = request.POST.copy()
        order_state = post_data.get('status', None)
        if order_state:
            qs = qs.filter(current_state=order_state)
        date_start = self.get_valid_date(post_data.get('start_date', None))
        date_end = self.get_valid_date(post_data.get('end_date', None))
        if date_start and date_end:
            if date_end < date_start:
                return JsonResponse({
                    'errors': True,
                    'message': 'Начальная дата не может быть меньше конечной даты',
                    'fields': ['start_date', 'end_date']
                })
        if date_start:
            qs = qs.filter(date__date__gte=date_start)
        if date_end:
            qs = qs.filter(date__date__lte=date_end)

        comment = post_data.get('comment', None)
        if comment:
            qs = qs.filter(comment__icontains=comment)

        if qs.exists():
            template = render_to_string(
                'account/includes/order_list.html',
                context={'orders': qs}
            )
        if not qs.exists():
            template = render_to_string(
                'account/includes/empty_order_list.html'
            )
        return JsonResponse({
            'errors': False,
            'template': template,
        })

    def get_valid_date(self, date_string):
        if not isinstance(date_string, str):
            return None

        try:
            datetime_value = datetime.strptime(date_string, self.date_format)
            return datetime_value
        except ValueError:
            return None

    def get_queryset(self):
        return Order.objects.filter(
            account__user=self.request.user,
            is_deleted=False,
            jurical=False).order_by("-id")

    def get_context_data(self):
        context = super(ListView, self).get_context_data()
        context['current_page'] = self.current_page
        context['order_states'] = OrderState.objects.all()
        return context


class JuricalOrdersList(OrdersList, LoginRequiredMixin):
    current_page = 'jurical'

    def render_to_response(self, context, **response_kwargs):
        # Закрытие доступа к юр. заказам для физ. лиц
        if not self.request.user.account.jurical:
            return django_redirect('/')
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        return Order.objects.filter(
            account__user=self.request.user,
            is_deleted=False,
            jurical=True
        ).order_by('-id')


class OrderDetail(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = Order
    context_object_name = 'order'
    template_name = 'account/order_detail.html'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        cart = Cart.objects.get(account__user=request.user)
        cart.clear()
        for item in order.order_items.all():
            cart.register_item(item)

        return JsonResponse({
            'errors': False,
            'redirect': reverse('order')
        })

    def get_object(self, queryset=None):
        request = self.request
        user = request.user
        try:
            obj = super(OrderDetail, self).get_object(queryset=queryset)
            if obj.account.user != user:
                raise Http404
            return obj
        except ObjectDoesNotExist:
            raise Http404


class OrderDeleteView(OrderDetail):

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if not order.is_in_stash:
            raise AttributeError('Нельзя удалить заказ, который не сохранен')
        order.remove()
        order.save()
        json_response = {
            'errors': False,
            'message': '',
            'redirect': ''
        }
        json_response['message'] = 'Заказ успешно удален'
        if order.jurical:
            json_response['redirect'] = reverse_lazy(
                'accounts:account-orders-jurical')
        elif not order.jurical:
            json_response['redirect'] = reverse_lazy('accounts:account-orders')
        return JsonResponse(json_response)


class OrderUpdateView(OrderDetail):
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        json_response = {
            'price': 'Цена товара',
            'total': 'Цена заказа',
            'is_overflowed': 'Флаг, кол-во твоара > остаток',
            'item_id': 'ИД для отображения уведомления о переполнении'
        }
        post_data = request.POST.copy()
        order_item_id = post_data.get('item_id', None)
        order_item = OrderItem.objects.get(id=order_item_id)
        count = post_data.get('product-count', 0)
        try:
            count = int(count)
        except ValueError:
            count = 0
        account = request.user.account
        order_item.update_count(count, account)
        json_response['price'] = order_item.total_price()
        json_response['total'] = order.count_order()
        json_response['is_overflowed'] = order_item.is_count_overflowed
        json_response['item_id'] = order_item.id
        return JsonResponse(json_response)


class OrderItemDeleteView(OrderDetail):
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        json_response = {
            'errors': "Флаг наличия ошибок",
            'message': "Сообщение от сервера",
            'total': "Полная стоимость заказа",
            'count': "Количество предметов в заказе"
        }
        post_data = request.POST.copy()
        order_item_id = post_data.get('item_id', None)
        order_item = OrderItem.objects.get(id=order_item_id)

        order_item.delete()
        total_price = order.count_order()
        json_response['errors'] = False
        json_response['message'] = "Товар успешно удален"
        json_response['total'] = total_price
        json_response['count'] = order.order_items.all().count()
        return JsonResponse(json_response)


class OrderToPdfView(OrderDetail):
    PDF_TEMPLATE_NAME = 'account/order-pdf.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object
        if order.account != request.user.account:
            return HttpResponseForbidden()
        template = get_template(self.PDF_TEMPLATE_NAME)
        context_data = self.get_context_data()
        html = template.render(context_data)
        options = {
            'quiet': ''
        }
        display = Display()
        try:
            display.start()
            pdf = pdfkit.from_string(html, False, options=options)
        finally:
            display.stop()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['retail_price'] = False
        # КП ИЛИ ПДФ
        # КП - отображаем розничную цену товаров
        # ПДФ - цена, заказа и товаров, как есть
        is_price_type_retail = self.request.GET.get('retail', False)
        if is_price_type_retail:
            context['retail_price'] = True

        return context

    def post(self, request, *args, **kwargs):
        raise NotImplementedError(
            'Для формирования пдф не определен метод POST')


class DataTemplate(TemplateView):
    """Страница с данными о пользователе в личном кабинете"""

    template_name = "account/data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["account"] = Account.objects.get(user=self.request.user)
        return context

    def render_to_response(self, context, **response_kwargs):
        # Закрытие доступа к личному кабинету для не авторизованных
        # пользователей
        if not self.request.user.is_authenticated:
            return django_redirect('/')
        return super().render_to_response(context, **response_kwargs)


class FavoritesTemplate(TemplateView):
    """Странца с избранными товарами личного кабинета"""

    template_name = "account/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites_page"] = True
        return context


class FavoritesWaitingList(ListView):
    """
    Страница со списком ожидаемых товаров относительно избранных товаров
    личного кабинета
    """

    model = FavoritesItem
    context_object_name = "waiting"
    template_name = "account/waiting.html"

    def get_queryset(self):
        favorites = Favorites.objects.get(account__user=self.request.user)
        return self.model.objects.filter(favorites=favorites, waiting=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites_page"] = True
        return context


class PasswordTemplate(TemplateView):
    """Страница смены пароля в личном кабинете"""

    template_name = "account/password.html"


class SubscribeTemplate(TemplateView):
    """Страница подписки в личном кабинете"""

    template_name = "account/subscribe.html"


# Ajax обработчики

class LoginView(View):
    """Обработчик запроса на вход в личный кабинет"""

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            redirect = reverse("accounts:account-orders")
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            auth = Account.auth_with_password(request, email, password)
            if not auth:
                try:
                    account = Account.objects.get(email=email)
                    return JsonResponse({
                        "errors": True,
                        "fields": {
                            "password": "Неверный пароль"
                        },
                        "message": "Неверный email или пароль"
                    })
                except:
                    return JsonResponse({
                        "errors": True,
                        "fields": {
                            "email": "Неверный email",
                            "password": "Неверный пароль"
                        },
                        "message": "Неверный email или пароль"
                    })
            return JsonResponse({"errors": False, "redirect": redirect})
        return JsonResponse({
            "errors": True,
            "fields": form.errors,
            "message": "Введите правильный адрес электронной почты."
        })


class CreateAccountView(TemplateView):
    template_name = 'account/register.html'

    def render_to_response(self, context, **response_kwargs):
        # Закрытие доступа к регистрации для авторизованных
        # пользователей
        if self.request.user.is_authenticated:
            return django_redirect('/')
        return super().render_to_response(context, **response_kwargs)


class RegisterView(View):
    """Регистрация пользователя в личном кабинете"""

    @method_decorator(check_recaptcha)
    def dispatch(self, *args, **kwargs):
        print('-' * 20, kwargs)
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def post(self, request):
        form = RegisterForm(request.POST)
        if not request.recaptcha_is_valid:
            return JsonResponse({
                "errors": True,
                "fields": {
                    'email': "Пройдите google recaptcha"
                }
            })
        if form.is_valid():
            email = form.cleaned_data['email']
            validator = Validator(form.cleaned_data, None)
            if validator.has_errors:
                return JsonResponse({
                    'errors': True,
                    'fields': validator.fields
                })
            user = Account.register(
                email, "{}://{}".format(request.scheme, request.META['HTTP_HOST']))
            if not user:
                return JsonResponse({
                    "errors": True,
                    "fields": {
                        'email': "Пользователь с таким email уже существует"
                    }
                })
            Account.fill_data(form.cleaned_data)
            Account.auth_with_password(
                request, user.email, form.cleaned_data['password'])
            return JsonResponse({
                "errors": False,
                "redirect": reverse("account-data"),
                "message": "Учетная запись успешно создана"
            })
        return JsonResponse({
            "errors": True,
            "fields": form.errors,
            "message": "Введите правильный адрес электронной почты."
        })


class ChangeDataView(View):
    """Обработчик изменения данных профиля пользователя"""

    def post(self, request, *args, **kwargs):
        error_list = {}
        fields = request.POST.copy()
        account = Account.objects.get(user=request.user)
        jurical = False
        phone = fields['phone']
        if '+' not in phone:
            phone = '+' + phone
            fields['phone'] = phone
        if fields["name"] == "":
            error_list["name"] = "Укажите имя"
        if fields["surname"] == "":
            error_list["surname"] = "Укажите фамилию"
        if fields.get('jurical', None) == "on":
            fields['jurical'] = True
            jurical = True
        user = request.user
        validator = Validator(fields, user)
        if validator.has_errors:
            return JsonResponse({
                'errors': True,
                'fields': validator.fields,
            })

        if not error_list:
            # account = Account.objects.get(user=request.user)
            account.name = fields["name"]
            account.surname = fields["surname"]
            account.middle_name = fields["middle_name"]
            account.phone = fields["phone"]
            account.email = fields["email"]
            account.jurical = jurical
            account.company_title = ''
            account.company_inn = ''
            if jurical:
                account.company_title = fields.get('company_title')
                account.company_inn = fields.get('company_inn')
            account.save()
            return JsonResponse({
                "errors": False,
                "message": "Данные успешно изменены",
                "redirect": reverse('accounts:account-data')
            })
        else:
            return JsonResponse({"errors": True, "fields": error_list})


class SubscribeAddView(View):
    """Обработчик добавления пользователя личного кабинета в подписчики"""

    def post(self, request, *args, **kwargs):
        try:
            Subscriber.objects.get(user=request.user).delete()
            return JsonResponse({"errors": False, "message": "Вы отписались"})
        except ObjectDoesNotExist:
            Subscriber.objects.create(user=request.user)
            return JsonResponse({"errors": False, "message": "Вы подписались"})


class ChangePasswordView(View):
    """
    Обработчик смены пароля пользоватекля Django к которому привязан личный
    кабинет.
    """

    def post(self, request):
        account = Account.objects.get(user=request.user)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            if not account.check_password(old_password):
                return JsonResponse({
                    "errors": True,
                    "fields": {"old_password": "Старый пароль введён неверно"}
                })
            account.user.set_password(form.cleaned_data["password"])
            account.user.save()
            Account.auth(request, account.user)
            return JsonResponse({
                "errors": False,
                "message": "Пароль успешно изменен"
            })
        # Возврат ошибок, если форма не прошла валидацию
        return JsonResponse({"errors": True, "fields": form.errors})


class LogoutView(View):
    """Обработчик выхода из пользователя линчого кабинета"""

    def get(self, request):
        Account.logout(request)
        return django_redirect('/')


class CustomPasswordResetView(PasswordResetView):
    # success_url: Optional[str] = reverse_lazy('accounts:password_reset_done')
    email_template_name = "account/password_reset_email.html"
    success_url: Optional[str] = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(TemplateView):
    template_name: str = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url: Optional[str] = reverse_lazy('index')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name: str = "index.html"
