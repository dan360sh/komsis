from django.db import models
from django.db.models import Sum
from mptt.models import MPTTModel

from .. import models as catalog_models
from ..models import Product


class Option(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", blank=False, on_delete=models.SET_NULL,
                                null=True, related_name="options")
    unloading_id = models.CharField(verbose_name="Ид 1С", blank=False, null=False,
                                    unique=True, max_length=50)
    active = models.BooleanField(
        verbose_name="Активность", default=True, db_index=True)
    title = models.CharField(verbose_name="Заголовок", blank=False, null=True,
                             max_length=300)
    step = models.FloatField(verbose_name='Шаг', default=1,)
    count = models.FloatField(
        verbose_name="Количество", default=0, blank=True)
    price = models.FloatField(verbose_name="Цена", blank=False, default=0,
                              null=True)
    # old_price = models.FloatField(verbose_name="Старая цена", blank=False, default=0,
    #                           null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "опция"
        verbose_name_plural = "Опции"
        ordering = ['id']

    def _get_total_count(self, attrs):
        return self.storages.filter(**attrs).aggregate(Sum('count'))['count__sum'] or 0

    def get_total_count(self):
        return self._get_total_count({})

    def get_count_vologda(self):
        return self._get_total_count({'storage__title': 'Вологда'})

    def get_count_cherepovets(self):
        return self._get_total_count({'storage__title': 'Череповец'})

    @property
    def default_price(self) -> float:
        price_type = self.prices.filter(
            type__id_1c=catalog_models.DEFAULT_PRICE
        ).first()
        # Если не удалось найти розничную цену
        # возвращается оптовая цена
        return price_type.value if price_type is not None else self.price

    def get_price_by_account(self, account):
        """Получить цену опции исходя из типа цены в акк."""
        # Могут удалить аккаунт, лол
        # чтобы не появлялось 500 ошибок
        # просто вернем ничего
        if not account:
            return self.price

        if account.is_price_type_default:
            return self.price

        prices_by_price_type = self.prices.filter(type=account.price_type)
        if not prices_by_price_type.exists():
            return self.price

        return prices_by_price_type.first().value
