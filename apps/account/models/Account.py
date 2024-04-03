import re
from decimal import *

from apps.catalog import models as catalog_models
from apps.catalog.models import DEFAULT_PRICE, get_default_price_type
from apps.configuration.models import Settings
from apps.feedback.utils import template_email_message
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import is_naive

from .Status import AccountStatus


class Account(models.Model):
    """
    Модель пользователя личного кабинета.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account")
    email = models.EmailField(default="", blank=True, max_length=100)
    name = models.CharField(verbose_name="Имя", blank=False, max_length=100)
    surname = models.CharField(verbose_name="Фамилия", blank=False,
                               max_length=100, default="")
    middle_name = models.CharField(verbose_name="Отчество", blank=True,
                                   max_length=100, default="")
    phone = models.CharField(verbose_name="Телефон",
                             blank=True, max_length=100)

    valid_phone = models.CharField(verbose_name="Проверенный номер телефона",
                                   max_length=100, null=True, blank=True)

    jurical = models.BooleanField(verbose_name='Является юр. лицом',
                                  default=False)
    company_title = models.CharField('Название компании', max_length=255,
                                     blank=True, default="")
    company_inn = models.CharField(
        'ИНН', max_length=25, blank=True, default="")
    manager = models.ForeignKey(
        'Manager',
        related_name='accounts',
        verbose_name='Менеджер',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    status = models.ForeignKey(AccountStatus, related_name="accounts",
                               verbose_name="Статус", on_delete=models.SET_DEFAULT,
                               default=AccountStatus.default)
    # default = Розница
    price_type = models.ForeignKey(
        catalog_models.PriceType,
        verbose_name='Отображаемый тип цены',
        default=get_default_price_type,
        on_delete=models.CASCADE
    )
    discount_card = models.ForeignKey(
        'DiscountCard',
        verbose_name="Скидочная карта",
        related_name="accounts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    points_total = models.FloatField(
        verbose_name="Количество баллов",
        validators=[
            MinValueValidator(0)
        ],
        default=0
    )
    unconfirmed_points = models.FloatField(
        verbose_name='Неподтвержденные баллы',
        help_text='''
            Эти баллы будут постепенно переходить на основной
            бонусный счет пользователя,
            по мере оплаты им его заказов
            ''',
        validators=[
            MinValueValidator(0)
        ],
        default=0
    )
    bonus_card_id = models.CharField(verbose_name="ИД бонусной карты",
                                     max_length=200, null=True, blank=True)
    purchase_sum = models.FloatField(verbose_name="Сумма всех покупок",
                                     default=0,
                                     validators=[MinValueValidator(0), ])
    id_1c = models.CharField(verbose_name="ИД из 1с",
                             null=True, blank=True, max_length=200)
    clear_name = models.CharField(verbose_name="Полное имя",
                                  null=True, blank=True, max_length=300)
    contract_name = models.CharField(verbose_name="Наименование договора",
                                     null=True, blank=True, max_length=300)
    contract_type = models.CharField(verbose_name="Тип договора",
                                     null=True, blank=True, max_length=300)
    contract_balance = models.FloatField(verbose_name="Баланс", default=0)

    def __str__(self):
        return self.user.username

    def check_password(self, password):
        user = authenticate(username=self.user.username, password=password)
        if user == self.user:
            return True
        return False

    def count_points(self, purchase_cost):
        percent = self.discount_card.get_discount
        purchase_cost = Decimal(purchase_cost)
        points_from_purchase = purchase_cost * percent
        return round(points_from_purchase, 2)

    def calculate_discount(self, purchase_cost, points):
        purchase_cost = Decimal(purchase_cost)
        points = Decimal(points)
        return round(purchase_cost - points, 2)

    def is_valid_points_amount(self, points_amount):
        points_amount = float(points_amount)
        return self.points_total >= points_amount

    def reduse_points(self, points_amount):
        points_amount = float(points_amount)
        self.points_total = self.points_total - points_amount
        self.points_total = round(self.points_total, 2)
        self.save()

    def append_points(self, points_amount):
        points_amount = float(points_amount)
        self.unconfirmed_points += points_amount
        self.unconfirmed_points = round(self.unconfirmed_points, 2)
        self.save()

    def update_uuid(self, value):
        assert value is not None
        self.id_1c = value
        self.save()

    def update_status(self, value: AccountStatus):
        if not isinstance(value, AccountStatus):
            raise TypeError(
                "Значение должно быть экземпляром класса AccountStatus")
        self.status = value
        self.save()

    def add_purchase_sum(self, value):
        assert value is not None
        assert isinstance(value, (int, float, Decimal)),\
            "Значение должно принадлежать числовому типу"
        self.purchase_sum += value
        self.purchase_sum = round(self.purchase_sum, 2)
        self.save()

    def get_remainder_to_next_status(self):
        next_status: AccountStatus = self.status.get_next()
        return round(next_status.min_limit - self.purchase_sum, 2)

    @property
    def start_points_value(self) -> int:
        """Получить стартовое значение бонусов,
        которые пользователь сможет потратить.

        Returns:
            int: Начальное кол-во бонусов
        """
        return int(self.points_total / 2)

    @property
    def is_price_type_default(self) -> bool:
        """Проверить, что аккаунт имеет дефолтный тип цены.

        Returns:
            bool: Результат проверки
        """
        return self.price_type.pk == DEFAULT_PRICE

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    @property
    def display_pdf_buttons(self):
        """Условие для отображения кнопок генерации пдф - тип цены пользователя."""
        # -  Eсловие, когда должны появляться кнопки КП и PDF:
        # Если тип цен пользователя равен Крупный опт, партнер или дилер
        DILLER_ID = 'a6bfe5d5-ccce-11dd-8d29-001fc6b4b87e'
        BIG_WHOLESALE_ID = 'a6bfe5d4-ccce-11dd-8d29-001fc6b4b87e'
        PARTNER_ID = 'a6bfe5d3-ccce-11dd-8d29-001fc6b4b87e'
        displayable_price_types = [DILLER_ID, BIG_WHOLESALE_ID, PARTNER_ID]

        return self.price_type.id_1c in displayable_price_types

    @staticmethod
    def auth(request, user):
        django_login(request, user)
        return user

    @staticmethod
    def auth_with_password(request, login, password):
        user = authenticate(username=login, password=password)
        if user:
            return Account.auth(request, user)
        return False

    @classmethod
    def register(cls, email, domain=None, send_mail=False):
        user, created = User.objects.get_or_create(username=email, email=email)
        if created is False:
            return False
        password = User.objects.make_random_password(10)
        user.set_password(password)
        user.save()
        user.account.email = email
        user.account.save()
        if not domain:
            try:
                site_name = Settings.objects.first().name
            except:
                site_name = ""
        else:
            site_name = domain
        if send_mail:
            template_email_message(
                "account/register-mail.html", subject="Регистрация на сайте",
                to=[email, ], data={'user': user, 'password': password,
                                    "site": site_name})
        return user

    @classmethod
    def find_by_name(cls, name):
        objects = cls.objects.filter(clear_name__icontains=name)
        if objects.exists():
            return objects.first()

    @classmethod
    def find_by_uuid(cls, uuid):
        objects = cls.objects.filter(id_1c=uuid)
        if objects.exists():
            return objects.first()

    @staticmethod
    def fill_data(data):
        email = data['email']
        user = User.objects.get(username=email)
        user.account.name = data['name']
        user.account.surname = data['surname']
        user.account.middle_name = data.get('middle_name', '')
        user.account.phone = data['phone']
        user.account.jurical = data['jurical']
        user.account.company_title = data['company_title']
        user.account.company_inn = data['company_inn']
        user.set_password(data['password'])
        user.save()
        user.account.save()
        return user.account

    @staticmethod
    def logout(request):
        """Выход из пользователя личного кабинета

        Arguments:
            request {HttpRequest} -- Запрос на сервер
        """

        django_logout(request)

    @staticmethod
    def get_valid_phone(phone_number):
        """Получить валидный номер телефона из обычного номера.

        Обычный номер - номер инстанса.

        Args:
            phone_number (str): "Грязный номер телефона", содержит +, -, (, )

        Returns:
            str: Строка без первой 8 или 7,
            а также без символов "Грязного номера"
        """
        # Удаляем лишние символы из номера
        clear_phone = re.sub('[^\d]', '', phone_number)

        PHONE_LENGTH = 11
        # Если номер телефона правильной длины
        # удаляем первый символ
        if len(clear_phone) == PHONE_LENGTH:
            # Так как с номера уже удалены +, (, ), -
            # то можно спокойно удалять первый символ
            clear_phone = clear_phone[1:]
        return clear_phone

    @classmethod
    def get_account(cls, phone=None, inn=None, email=None):
        """Получить акканут по телефону, почте или ИНН.

        Args:
            phone (str, optional): Номер телефона. Defaults to None.
            inn (str, optional): ИНН. Defaults to None.
            email (str, optional): Email. Defaults to None.

        Raises:
            ValueError: Если ни одно из значений не было передано

        Returns:
            Account: Найденный инстанс
            None: Если ничего найдено не было
        """
        if all(field is None or field == '' for field in [phone, inn, email]):
            raise ValueError("Хотя бы одно из значений должно быть передано")

        if email is not None and email != "":
            accounts = cls.objects.filter(email=email)
            if accounts.exists():
                return accounts.first()

        if inn is not None and inn != "":
            accounts = cls.objects.filter(company_inn=inn)
            if accounts.exists():
                return accounts.first()

        if phone is not None and phone != "":
            accounts = cls.objects.filter(valid_phone=phone)
            if accounts.exists():
                return accounts.first()

        return None

    @classmethod
    def get_clear_name(self, account):
        clear_name: str = account.surname
        clear_name += " " + account.name
        clear_name += " " + account.middle_name
        return clear_name

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """Создание новой модели пользователя личного кабинета.

    Пользователь личного кабинета создается по сигнялу сохранения стандартного
    пользователя Django `django.contrib.auth.models.User`. Пользователь
    личного кабинета будет создан только в том случае если пользователь Django
    на момент сохранения был создан.

    Arguments:
        sender {Model} -- Модель пользователя Django
        instance {DjangoObject} -- Экземпляр пользователя Django
        created {bool} -- Показывает был ли создан пользователь Django
    """

    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    """Сохранение уже существующего пользователя личного кабинета.

    Пользователь личного кабинета сохраняется по сигнялу сохранения
    пользователя Django.

    Arguments:
        sender {Model} -- Модель пользователя Django
        instance {[type]} -- Экземпляр пользователя Django
    """

    instance.account.save()


@receiver(pre_save, sender=Account)
def remove_product_items(sender, instance, **kwargs):
    """Удаление всех товаров из корзины, избранного
    по изменению выбранного типа цены.
    """
    # Только если пользователь не был создан только что
    if instance.id is not None:
        previous_instance = sender.objects.get(id=instance.id)
        if previous_instance.price_type != instance.price_type:
            instance.favorites.favorites_items.all().delete()
            instance.cart.cart_items.all().delete()


@receiver(pre_save, sender=Account)
def set_valid_phone(sender, instance, **kwargs):
    """Установить аккаунту валидный номер телефона
    по сигналу.

    Валидный номер - номер, без (, ), +, -, 7 и 8 в начале

    Args:
        sender (Model): Модель пользователя Django
        instance ([type]): Экземпляр пользователя Django
    """
    # Если каким-то образом сохранился инстанс без номера - скип
    if instance.phone is None or instance.phone == "":
        pass

    elif instance.phone is not None or instance.phone != "":
        instance.valid_phone = sender.get_valid_phone(instance.phone)


@receiver(pre_save, sender=Account)
def update_clear_name(sender: Account.__class__, instance: Account, **kwargs):
    instance.clear_name = Account.get_clear_name(instance)
