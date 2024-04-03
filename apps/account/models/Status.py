from django.db import models


class AccountStatus(models.Model):
    LOYAL = "000000002"
    NEW = "000000001"
    VIP = "000000003"
    CODES = (
        (LOYAL, "LOYAL"),
        (NEW, "NEW"),
        (VIP, "VIP")
    )

    title = models.CharField(verbose_name="Наименование", max_length=200)
    image = models.ImageField(verbose_name="Изображение", null=True)
    min_limit = models.PositiveIntegerField(verbose_name="Минимальный порог")
    max_limit = models.PositiveIntegerField(verbose_name="Максимальный порог",
                                            null=True, blank=True)
    previous_status = models.ForeignKey("self",
                                        verbose_name="Предыдущий статус",
                                        null=True, blank=True, on_delete=models.SET_NULL,)
#    code = models.CharField(verbose_name="Код", max_length=200,
#                            choices=CODES, default=NEW)

    @classmethod
    def default(cls):
        objects = cls.objects.filter(previous_status__isnull=True)
        if objects.exists():
            return objects.first().id

        DEFAULT_MAX = 50_000
        default_object = cls.objects.create(title="NEW", min_limit=0,
                                            max_limit=DEFAULT_MAX)
        return default_object.id

    def __str__(self) -> str:
        return self.title

    def get_next(self):
        if self.is_last:
            return None
        next = AccountStatus.objects.filter(previous_status=self)
        return next.first() if next.exists() else None

    @property
    def is_last(self):
        return self.max_limit is None or self.max_limit == 0

    class Meta:
        verbose_name = "Статус аккаунта"
        verbose_name_plural = "Статусы акканута"
