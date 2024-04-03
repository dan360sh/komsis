from django.db import models
from django.db.models import Avg, Max, Min

from .. import models as catalog_models

types_attrs = (
    (0, "Справочник"),
    (1, "Число")
)


class AttributesGroup(models.Model):
    unloading_id = models.CharField('Идентификатор выгрузки', blank=True,
                                    default='', max_length=300)
    title = models.CharField(verbose_name="Заголовок", blank=False, null=True,
                             max_length=300)
    type_value = models.IntegerField(verbose_name="Тип атрибута",
                                     choices=types_attrs, default=0)
    show = models.BooleanField(verbose_name="Показывать в категориях",
                               default=True)
    show_parent = models.BooleanField(
        verbose_name="Показывать в родительских категориях", default=True)
    show_in_header = models.BooleanField(
        verbose_name="Показывать фильтр в шапке каталога",
        default=False,
    )

    def __str__(self):
        return self.title

    def search_attributes(self, products):
        """
        Поиск атрибутов относительно товаров(`products`)
        """
        attribute_model = Attribute

        attributes = []

        if self.type_value == 0:
            attrs = self.attributes.filter(group__show=True,
                                           product__in=products).order_by('value', 'sort').distinct('value')
            for attr in attrs:
                attributes.append({
                    'title': attr.value.title,
                    'name': self.name,
                })

            date = {
                "group": self.title,
                "count": attrs.count(),
                "attributes": attributes
            }
        else:
            attrs = self.num_attributes.filter(group__show=True,
                                               product__in=products).order_by('value', 'sort').distinct('value')
            value_info = self.num_attributes.filter(product__in=products).aggregate(min_value=Min('value'),
                                                                                    max_value=Max('value'))
            if not value_info['min_value']:
                value_info['min_value'] = 0
            if not value_info['max_value']:
                value_info['max_value'] = 0
            name_input = 'nm_' + str(self.id) + '_i'
            min_value = {'val': int(
                value_info['min_value']), 'name_input': name_input}
            name_input = 'nm_' + str(self.id) + '_a'
            max_value = {'val': int(
                value_info['max_value']), 'name_input': name_input}

            date = {
                "group": self.title,
                "num_values": {'min_value': min_value, 'max_value': max_value}
            }

        return date

    def search_input_names(self, products):
        """
        Поиск атрибутов относительно товаров(`products`)
        """
        attribute_model = Attribute

        attributes = []

        attrs = self.attributes.filter(group__show=True,
                                       product__in=products).order_by('value', 'sort')
        for attr in attrs:
            attributes.append('ch_' + str(self.id) + '_' + str(attr.value.id))

        return attributes

    class Meta:
        verbose_name = "группа атрибутов"
        verbose_name_plural = "Группы атрибутов"


class AttributeValue(models.Model):
    unloading_id = models.CharField('Идентификатор выгрузки', blank=True,
                                    default='', max_length=300)
    title = models.TextField(verbose_name="Заголовок", blank=False, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"
        ordering = ["title"]


class Attribute(models.Model):
    unloading_id = models.CharField('Идентификатор выгрузки', blank=True,
                                    default='', max_length=300)
    sort = models.IntegerField("Сортировка", blank=False, default=1)
    product = models.ForeignKey(catalog_models.Product, verbose_name="Товар",
                                blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='product_attrbutes')
    group = models.ForeignKey(AttributesGroup, verbose_name="Группа",
                              blank=False, null=True, on_delete=models.SET_NULL,
                              related_name='attributes')
    value = models.ForeignKey(AttributeValue, verbose_name="Значение",
                              blank=False, null=True, on_delete=models.SET_NULL,
                              related_name="value_attrbutes")
    name = models.CharField('Сериализованное значение', blank=True,
                            default='', max_length=300)

    def __str__(self):
        if self.product and self.group:
            return str(self.product.title) + " - " + str(self.group.title) \
                + " - " + str(self.value.title)
        elif self.group:
            return str(self.group.title) + " - " + str(self.value.title)
        return str(self.value.title)

    def save(self, *args, **kwargs):
        if self.group.type_value == 1:
            try:
                int(self.value.title)
            except ValueError:
                try:
                    float(self.value.title)
                except ValueError:
                    self.value = None
        if not self.name:
            self.name = 'ch_{}_{}'.format(
                str(self.group.id), str(self.value.id))
        super(Attribute, self).save(*args, **kwargs)
        category = self.product.category
        group = self.group
        # if category:
        #     products = catalog_models.Product.objects.\
        #                         filter(category=category)
        #     fields = ({'unloading_id': "",})
        #     value,created = catalog_models.AttributeValue.objects.\
        #         get_or_create(title="Не указано", defaults=fields)
        #     for product in products:
        #         try:
        #             attr = catalog_models.Attribute.objects\
        #                     .get(product=product,group=group)
        #         except:
        #             attr = catalog_models.Attribute.objects\
        #             .create(product=product,group=group, value=value)

    class Meta:
        verbose_name = "атрибут"
        verbose_name_plural = "Атрибуты"
        ordering = ["product", "sort"]


class NumAttribute(models.Model):
    unloading_id = models.CharField('Идентификатор выгрузки', blank=True,
                                    default='', max_length=300)
    sort = models.IntegerField("Сортировка", blank=False, default=1)
    product = models.ForeignKey(catalog_models.Product, verbose_name="Товар",
                                blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='product_num_attrbutes')
    group = models.ForeignKey(AttributesGroup, verbose_name="Группа",
                              blank=False, null=True, on_delete=models.SET_NULL,
                              related_name='num_attributes')
    value = models.FloatField(verbose_name="Значение атрибута")

    def __str__(self):
        if self.product and self.group:
            return str(self.product.title) + " - " + str(self.group.title) \
                + " - " + str(self.value)
        elif self.group:
            return str(self.group.title) + " - " + str(self.value)
        return str(self.value)

    class Meta:
        verbose_name = "Числовой атрибут"
        verbose_name_plural = "Числовые атрибуты"
        ordering = ["product", "sort"]
