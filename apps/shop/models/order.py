from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.query_utils import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import datetime
from filer.fields.image import FilerFileField

from apps.account.models import Account
from apps.catalog.models import Color, Option, Product

from .order_state import OrderState


class Order(models.Model):
    """
    Модель заказа товаров
    """

    # Стадии заказа
    STATUSES = (
        ("processing", "В обработке"),
        ("completed", "Выполнен"),
        ("canceled", "Отменен"),
        ("stash", "Сохранен"),
    )

    SHIPPINGS = (
        ("self", "Самовывоз"),
        ("transport", "Транспотной компанией"),
        ("post", "Почтой"),
        ("courier", "Курьером"),
        ("dostavka", "Доставка"),
    )

    PAYMENTS = (
        ("bank", "Банковской картой онлайн"),
        ("bill", "Оплата по счету"),
        ("receiving", "Оплата при получении"),
    )

    UPLOAD = (
        ("doNotUpload", "Не подлежит выгрузке"),
        ("not_upload", "Не выгружен"),
        ("upload", "Выгружен"),
        ("processing", "В процессе"),
    )

    account = models.ForeignKey(
        Account,
        verbose_name="Профиль",
        blank=True,
        null=True,
        related_name="orders",
        on_delete=models.SET_NULL,
    )
    surname = models.CharField(
        verbose_name="Фамилия", default="", blank=True, max_length=100
    )
    name = models.CharField(verbose_name="Имя", default="", blank=True, max_length=300)
    middle_name = models.CharField(
        verbose_name="Отчество", default="", blank=True, max_length=300
    )
    phone = models.CharField(
        verbose_name="Телефон", default="", blank=True, max_length=300
    )
    email = models.EmailField(verbose_name="Email", default="", blank=False)
    comment = models.TextField(verbose_name="Комментарий", blank=True, max_length=300)
    date = models.DateTimeField(verbose_name="Дата заказа", default=datetime.now)
    total = models.FloatField(
        verbose_name="Общая стоимость заказа", null=True, blank=True
    )
    bank_id = models.CharField(
        verbose_name="Ид заказа в системе банка", default="", blank=True, max_length=100
    )
    payment = models.BooleanField(verbose_name="Заказ оплачен", default=False)
    status = models.CharField(
        verbose_name="Статус", choices=STATUSES, default="processing", max_length=50
    )
    type_payment = models.CharField(
        verbose_name="Способ оплаты",
        choices=PAYMENTS,
        default="receiving",
        max_length=50,
    )
    shipping = models.CharField(
        verbose_name="Доставка", choices=SHIPPINGS, default="self", max_length=50
    )
    shipping_price = models.FloatField(verbose_name="Стоимость доставки", default=0)
    post_code = models.PositiveIntegerField(
        verbose_name="Почтовый индекс", null=True, blank=True
    )
    region = models.CharField(
        verbose_name="Область", default="", blank=True, max_length=200
    )
    district = models.CharField(
        verbose_name="Район", default="", blank=True, max_length=200
    )
    city = models.CharField(
        verbose_name="Нас. пункт", default="", blank=True, max_length=200
    )

    street = models.CharField(
        verbose_name="Улица", default="", blank=True, max_length=200
    )
    house = models.CharField(verbose_name="Дом", default="", blank=True, max_length=200)
    housing = models.CharField(
        verbose_name="Корпус", default="", blank=True, max_length=100
    )

    apartment = models.CharField(
        verbose_name="Квартира", default="", blank=True, max_length=50
    )
    entrance = models.CharField("Подъезд", default="", blank=True, max_length=50)
    # WTF 2 comment oO
    comment = models.TextField(verbose_name="Комментарий", default="", blank=True)

    shipping_type_name = models.CharField(
        verbose_name="Способ доставки", default="", blank=True, max_length=50
    )

    status_imported = models.CharField(
        "Загружены в 1С",
        default="not_upload",
        editable=True,
        choices=UPLOAD,
        max_length=25,
    )

    shop_address = models.CharField(
        "Адрес магазина", default="", blank=True, max_length=255
    )

    company_title = models.CharField(
        "Название компании", default="", blank=True, max_length=125
    )
    company_inn = models.CharField(
        "ИНН компании", default="", blank=True, max_length=125
    )
    payment_file = models.FileField(
        "Реквизиты", default="", blank=True, upload_to="files/payment/"
    )

    jurical = models.BooleanField("Заказ от юр. лица", default=False)

    total_without_points = models.FloatField(
        verbose_name="Стоимость заказа без вычета бонусов",
        validators=[MinValueValidator(0)],
        default=0,
    )

    points_spent = models.FloatField(
        verbose_name="Количество потраченных бонусов",
        validators=[MinValueValidator(0)],
        default=0,
    )

    points_collected = models.FloatField(
        verbose_name="Количество баллов, которые пользователь получит после оплаты",
        validators=[MinValueValidator(0)],
        default=0,
    )

    is_deleted = models.BooleanField(
        verbose_name="Заказ удален?",
        default=False,
        help_text="Вместо удаления заказа отметьте этот пункт",
    )

    is_confirmed = models.BooleanField(
        verbose_name="Заказ был подтевержден",
        default=False,
        help_text=(
            "Техническое поле необходимое для"
            "обновления поля 'сумма покупок'"
            "у пользовтеля, совершившего заказ"
        ),
    )

    current_state = models.ForeignKey(
        OrderState,
        verbose_name="Текущее состояние заказа",
        on_delete=models.SET_DEFAULT,
        default=OrderState.default,
        related_name="orders",
    )

    completed_states = models.ManyToManyField(
        OrderState, verbose_name="Выполненные состояния", related_name="passed_orders"
    )

    def __str__(self):
        return "Заказ № " + str(self.id)

    def str_type_payment(self):
        return dict(Order.PAYMENTS)[self.type_payment]

    def str_shipping(self):
        return dict(Order.SHIPPINGS)[self.shipping]

    def status_value(self):
        """Получаем значение статуса заказа относительно его ключа.

        Returns:
            str -- Значение статуса заказа
        """

        return dict(self.STATUSES)[self.status]

    def get_filename(self):
        if self.payment_file:
            return self.payment_file.name.split("/")[-1]
        return ""

    def is_shipping_default(self):
        return self.shipping == "self"

    def get_shipping_address(self):
        return f"{self.region}, подъезд №{self.entrance}"

    def save_in_stash(self):
        """Пометить заказ, как сохраненный."""
        self.status = "stash"
        self.save()

    def remove_from_stash(self):
        self.status = "processing"
        self.save()

    @property
    def should_send_email(self) -> bool:
        """Проверка на то, что сообщение о создании заказа
        должно быть отправлено.

        Returns:
            bool: Результат проверки
        """
        return not self.is_in_stash and self.type_payment != "bank"

    @property
    def is_in_stash(self):
        """Проверка заказа на то, что он сохранен."""
        return self.status == "stash"

    def update_fields(self, data):
        self.district = data.get("district", "")
        self.city = data.get("city", "")
        self.street = data.get("street", "")
        self.house = data.get("house", "")
        self.housing = data.get("housing", "")
        self.apartment = data.get("apartment", "")
        self.comment = data.get("comment", "")
        self.type_payment = data.get("payment")
        self.shipping_price = data.get("calculated_shipping_price")
        self.payment_file = data.get("payment_file", None)
        self.status = "processing"
        self.shipping_type_name = data.get("shipping_title", "")
        self.shipping = data.get("shipping_code", "")
        self.region = data.get("region", "")
        self.entrance = data.get("entrance", "")
        self.status_imported = data.get("status_imported", "")
        self.jurical = data.get("jurical", False)
        self.save()

    def remove(self):
        self.is_deleted = True
        self.status_imported = "doNotUpload"
        return self

    def count_order(self):
        items = self.order_items.all()
        self.total = 0
        new_total = 0
        for item in items:
            new_total += item.total_price()
        self.total = round(new_total, 2)
        self.save()
        return self.total

    def set_date(self):
        """Обновление даты заказа."""
        self.date = datetime.now()
        self.save()

    def get_default_total(self):
        """Получить полную стоимость заказа,
        рассчитанную по дефолтной цене.

        Returns:
            float: Стоимость заказа
        """
        total_price = 0
        for item in self.order_items.all():
            item_price = item.option.price if item.option else item.product.price
            count = item.count
            total_price += round(item_price * count, 2)
        return total_price

    def add_completed_state(self, state: OrderState):
        """Добавить к заказу выполненное состояние.

        Если было передано состояние, которое уже
        находится среди выполенных состояний текущего
        заказа, то исключение поднято не будет, но
        новое состояние также не будет добавлено

        Args:
            state (OrderState): Новое состояние
        """
        assert isinstance(
            state, OrderState
        ), "Значение должно быть экземпляром класса OrderState"

        if state in self.completed_states.all():
            return
        self.completed_states.add(state)
        self.save()

    @property
    def person_fullname(self):
        return f"{self.surname} {self.name} {self.middle_name}"

    @property
    def is_online_payment_available(self) -> bool:
        """Проверка заказа на возможность онлайн оплаты.

        Returns:
            bool: Результат проверки
        """
        return self.total != 0 and not self.jurical and not self.is_in_stash

    def set_current_state(self, state: OrderState):
        """Установить текущее состояние заказа

        Args:
            state (OrderState): Новое состояие
        """
        assert isinstance(
            state, OrderState
        ), "Значение должно принадлежать классу OrderState"
        self.current_state = state
        self.save()

    @property
    def has_confirmed_state(self) -> bool:
        """Проверка заказа, на то, что он имеет
        статус подтвержден.

        Returns:
            bool: Результат проверки
        """
        # счетчик до перехода на новый уровень будем брать
        # от количества заказов со статусами "отгружен(полностью/частично)
        qs = self.completed_states.filter(
            Q(code=OrderState.FULLY_SHIPPED) | Q(code=OrderState.PARTIALLY_SHIPPED)
        )
        return qs.exists()

    def mark_as_confirmed(self):
        """Пометить заказ, как подтвержденный."""
        if self.is_confirmed is True:
            return
        self.is_confirmed = True
        self.save()

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    """
    Модель элемента заказа.
    """

    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        null=True,
        blank=True,
        related_name="product_order_items",
        on_delete=models.SET_NULL,
    )
    color = models.ForeignKey(
        Color,
        verbose_name="Опция",
        null=True,
        blank=True,
        related_name="color_order_items",
        on_delete=models.SET_NULL,
    )
    option = models.ForeignKey(
        Option,
        verbose_name="Характеристка товара",
        null=True,
        blank=True,
        related_name="option_order_items",
        on_delete=models.CASCADE,
    )
    count = models.IntegerField(verbose_name="Количество", default=0)
    total = models.FloatField(
        verbose_name="Цена на момент покупки", blank=True, default=0
    )

    def __str__(self):
        return str(self.order)

    def total_price(self):
        return round(self.total * self.count, 2)

    def update_count(self, count, account=None):
        new_value = count
        if new_value > self.product.count:
            if (
                account is not None
                and account.jurical
                and self.product.is_able_to_overflow_count
            ):
                self.count = count
            else:
                self.count = self.product.count
            self.save()
            return

        if new_value < 1:
            self.count = 1
            self.save()
            return

        self.count = count
        self.save()

    def get_default_price(self):
        """Получить цену по умолчанию, которая всегда
        сохраняется в инстанс продукта.

        Returns:
            float: Цена инстанса продукта.
        """
        return self.product.price

    def get_default_total_price(self):
        if self.option:
            return round(self.option.price * self.count, 2)

        return round(self.product.price * self.count, 2)

    @property
    def is_count_overflowed(self):
        return self.count > self.product.count

    @property
    def is_paid(self):
        return self.current_state == OrderState.PAID

    class Meta:
        verbose_name = "элемент заказа"
        verbose_name_plural = "Элементы заказа"


@receiver(pre_save, sender=Order)
def on_order_change(sender, instance, **kwargs):
    """Добавляем или удаляем бонусы пользователю.

    `instance` - Образец Order до сохранения
    """
    if instance.id is None:
        # Скиапем, если заказ только создан
        return
    if instance.account is None:
        return
    if not instance.account.discount_card:
        # Скипаем, если к инстансу не подвязана карта
        return
    # is_paid - булево, прошлое состояние оплаты закааз
    # false - не оплачн
    # true - уже был оплачен, в этом случае все скипаем
    previous_instance = sender.objects.get(id=instance.id)
    is_paid = previous_instance.payment
    if is_paid or is_paid == instance.payment:
        # Если заказ уже был оплачен или
        # is_paid == состоянию инстанса - скип
        pass
    elif not is_paid and instance.payment:
        account = instance.account
        points_amount = instance.points_collected
        account.unconfirmed_points -= points_amount
        account.points_total += points_amount
        account.save()


@receiver(pre_save, sender=Order)
def on_order_paid(sender, instance: Order, **kwargs):
    """Обновление суммы покупок у пользователя.

    Поле будет обновлено только, если поле заказа `is_confirmed`
    имеет значение True.

    Повторного обновления поля, при нескольких
    сохранениях одинакового состояния `is_confirmed` происходить не будет.
    """
    if instance.id is None:
        return
    if instance.account is None:
        return
    prev_instance: Order = sender.objects.get(id=instance.id)
    if prev_instance.is_confirmed == instance.is_confirmed:
        return
    if instance.is_confirmed is False:
        return
    instance.account.add_purchase_sum(instance.total)


class OrderLog(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_created=True)
    log_file = FilerFileField(
        verbose_name="Лог", related_name="order_log_files", on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")

    class Meta:
        verbose_name = "Лог-файл заказа"
        verbose_name_plural = "Лог-файлы заказа"

    def __str__(self) -> str:
        return f"Лог №{self.id}"
        return f"Лог №{self.id}"
