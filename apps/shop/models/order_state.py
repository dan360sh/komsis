from django.db import models


class OrderState(models.Model):
    # Const
    RESERVED = "000000002"
    PAYMENT_AWAIT = "000000003"
    CONFIRMATION_AWAIT = "000000008"
    PAID = "000000004"
    PARTIALLY_SHIPPED = "000000005"
    FULLY_SHIPPED = "000000006"
    CANCELED = "000000007"
    ACCEPTED = "000000001"
    PARTIALLY_PAID = "000000009"

    DEFAULT_CODE = ACCEPTED

    CODES = (
        (ACCEPTED, "Принят"),
        (RESERVED, "Обработан, зарезервирован"),
        (PAYMENT_AWAIT, "Ожидает оплаты"),
        (CONFIRMATION_AWAIT, "Ожидает подтверждения"),
        (PAID, "Оплачен"),
        (PARTIALLY_SHIPPED, "Отгружен частично"),
        (FULLY_SHIPPED, "Отгружен полностью"),
        (CANCELED, "Отменен"),
        (PARTIALLY_PAID, "Оплачен частично")
    )

    title = models.CharField(max_length=200, verbose_name="Наименование")
    code = models.CharField(unique=True, max_length=200, verbose_name="Код",
                            choices=CODES, default=ACCEPTED)
    position = models.PositiveIntegerField()
#    color = models.CharField(verbose_name="Цвет", max_length=200,
#                             help_text="Цвет, которым будет выделен статус в ЛК",
#                             default="#f5a623")

    def __str__(self) -> str:
        return self.title

    @classmethod
    def default(cls):
        objects = cls.objects.filter(code=cls.ACCEPTED)
        if objects.exists():
            return objects.first().id

        default_object = cls.objects.create(title="Принят", code=cls.DEFAULT_CODE,
                                            position=1)
        return default_object.id

    class Meta:
        verbose_name = "Состояние заказа"
        verbose_name_plural = "Состояния заказа"
        ordering = ["position", "id"]
