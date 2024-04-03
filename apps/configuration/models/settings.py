from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

MODES = (
    ("", "Онлайн оплата отсутствует"),
    ("https://3dsec.sberbank.ru/payment/", "Тестовый режим"),
    ("https://securepayments.sberbank.ru/payment/", "Боевой режим"),
)


class SettingsBase(models.Model):
    """Базовая модель настроек сайта"""

    PRODUCT_VIEWS = (
        ('classic', 'Классик'),
        ('wide', 'Широкие'),
    )
    SOCIAL_VIEWS = (
        ('classic', 'Плитка'),
        ('column', 'Столбец'),
    )

    # Язык сделан уникальным для того, что бы можно было сделать настройки
    # относительно системных настроек языка в django, или для мультиязычности
    language = models.CharField(choices=settings.LANGUAGES, max_length=32,
                                unique=True, verbose_name=_('Язык'))

    # Основные настройки сайта

    name = models.CharField(verbose_name="Наименование сайта", null=False,
                            blank=True, max_length=300, default="")
    full_address = models.CharField(verbose_name="Полный адрес", default="",
                                    max_length=300, blank=True)
    address = models.CharField(verbose_name="Адрес", max_length=300,
                               default="", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=False)
    phones = models.CharField(verbose_name="Номера телефонов",
                              help_text="разделитель ;", default="",
                              blank=True, max_length=300)
    time_work = models.CharField(verbose_name="Режим работы", max_length=300,
                                 default="", blank=True)
    time_work_cherep = models.CharField(verbose_name="Режи работы, Череповец",
                                        max_length=300, default="", blank=True)
    coord_x = models.FloatField(verbose_name="Координата X на карте",
                                blank=True, null=True)
    coord_y = models.FloatField(verbose_name="Координата Y на карте",
                                blank=True, null=True)
    price_list = FilerFileField(
        verbose_name="Прайс лист", blank=True, null=True,
        related_name="catalog_company", on_delete=models.SET_NULL,
        help_text="Узнайте о нас больше")
    privacy_policy = RichTextUploadingField(
        verbose_name="Политика конфиденциальности", default="", blank=True)
    personal_data = RichTextUploadingField(
        verbose_name="Согласие на обработку персональных данных", default="", blank=True)
    color_scheme = ColorField(default='#006EFF',
                              verbose_name="Цветовая схема сайта", max_length=7,
                              help_text=_(u'HEX color, as #RRGGBB'))
    color_scheme_alpha = models.CharField(blank=True,
                                          verbose_name="Цветовая схема c alpha", max_length=50,
                                          default='rgba(0, 110, 255, 0.6)', )
    color_scheme_dark = models.CharField(blank=True, default='#000CD4',
                                         verbose_name="Цветовая схема затемнение", max_length=7, )
    in_product_view = models.CharField(verbose_name="Вид отображения похожих товаров",
                                       max_length=300, blank=False, choices=PRODUCT_VIEWS,
                                       default="classic")
    # Социальные сети

    social_view = models.CharField(verbose_name="Вид отображения соц. сетей",
                                   max_length=300, blank=False, choices=SOCIAL_VIEWS,
                                   default="classic")
    vkontakte = models.CharField(verbose_name="Ссылка на ВК группу",
                                 max_length=300, blank=True)
    facebook = models.CharField(verbose_name="Ссылка на fb группу",
                                max_length=300, blank=True)
    instagram = models.CharField(verbose_name="Ссылка на instagram",
                                 max_length=300, blank=True)
    telegram = models.CharField(verbose_name="Ссылка на telegram",
                                max_length=300, blank=True)
    twitter = models.CharField(verbose_name="Ссылка на twitter",
                               max_length=300, blank=True)
    youtube = models.CharField(verbose_name="Ссылка на youtube",
                               max_length=300, blank=True)
    odnoklassniky = models.CharField(verbose_name="Ссылка на Одноклассники",
                                     max_length=300, blank=True)
    # Настройки SEO

    seo_text = RichTextUploadingField(verbose_name="SEO текст", default="",
                                      blank=True)
    seo_img1 = FilerImageField(verbose_name="SEO картинка 1", null=True,
                               blank=True, related_name="seo_img1",
                               on_delete=models.SET_NULL)
    seo_img2 = FilerImageField(verbose_name="SEO картинка 2", null=True,
                               blank=True, related_name="seo_img2",
                               on_delete=models.SET_NULL)
    seo_img3 = FilerImageField(verbose_name="SEO картинка 3", null=True,
                               blank=True, related_name="seo_img3",
                               on_delete=models.SET_NULL)
    meta_title = models.CharField(verbose_name="SEO Заголовок", max_length=300,
                                  null=False, blank=True, default="")
    meta_description = models.TextField(verbose_name="Meta Description",
                                        default="", blank=True)
    meta_template_description = models.TextField(
        verbose_name="Meta template Description", default="", blank=True)
    meta_keywords = models.TextField(verbose_name="Meta Keywords", default="",
                                     help_text="вводить через запятую",
                                     blank=True)
    meta_template_title = models.CharField(
        verbose_name="Шаблон для сайта", default="", blank=True,
        max_length=300, help_text=""" ||site|| - имя сайта,
        ||object|| - имя объекта """)
    robots_txt = models.TextField(verbose_name="robots.txt", default="",
                                  blank=True)
    head_scripts = models.TextField(verbose_name="Вывод в head", default="",
                                    blank=True)
    scripts = models.TextField(verbose_name="Скрипты под footer", default="",
                               blank=True)

    # Сбербанк эквайринг

    mode_payment = models.CharField(verbose_name="Режим оплаты", choices=MODES,
                                    default="", max_length=100, blank=True)
    shop_id = models.CharField(verbose_name="Логин api", blank=True,
                               default="", max_length=100)
    api_key = models.CharField(verbose_name="Ключ api", blank=True,
                               default="", max_length=100)

    banner_text = models.CharField(verbose_name="текст баннера", blank=True,
                                   default="", max_length=300)
    banner_img = FilerImageField(verbose_name="изображение в баннере", null=True,
                                 blank=True, related_name="banner_img",
                                 on_delete=models.SET_NULL)

    payment_text = models.TextField(verbose_name="Текст 'Оплата' в карточке товара", blank=True,
                                    default="")
    shipping_text = models.TextField(verbose_name="Текст 'Доставка' в карточке товара", blank=True,
                                     default="")

    # bitrix24

    bitrix24_key = models.CharField(verbose_name="Ключ вебхуков bitrix24",
                                    blank=True, default="", max_length=100)
    bitrix24_domain = models.CharField(verbose_name="Домен третьего уровня",
                                       blank=True, default="", max_length=100,
                                       help_text="Пример: placestart.bitrix24.ru")

    def save(self, *args, **kwargs):
        color_scheme_alpha = "rgba({}, {}, {}, 0.6)".format(
            self._convert_base(self.color_scheme[1:3]),
            self._convert_base(self.color_scheme[3:5]),
            self._convert_base(self.color_scheme[5:7])
        )
        color_scheme_dark = self._darken(self.color_scheme)
        self.color_scheme_alpha = color_scheme_alpha
        self.color_scheme_dark = color_scheme_dark
        # Call the real save() method
        super(SettingsBase, self).save(*args, **kwargs)

    def get_seo_alt1(self):
        if self.seo_img1:
            if self.seo_img1.default_alt_text:
                return self.seo_img1.default_alt_text
            else:
                return self.seo_img1.original_filename
        return ""

    def get_seo_alt2(self):
        if self.seo_img2:
            if self.seo_img2.default_alt_text:
                return self.seo_img2.default_alt_text
            else:
                return self.seo_img2.original_filename
        return ""

    def get_seo_alt3(self):
        if self.seo_img3:
            if self.seo_img3.default_alt_text:
                return self.seo_img3.default_alt_text
            else:
                return self.seo_img3.original_filename
        return ""

    def get_phones(self):
        if self.phones:
            return self.phones.split(';')
        return ''

    def get_addresses(self):
        if self.address:
            return self.address.split(';')
        return ''

    def get_phone(self):
        if self.get_phones():
            return self.get_phones()[0]
        return ''

    def get_coord_x(self):
        return str(self.coord_x).replace(",", ".")

    def get_coord_y(self):
        return str(self.coord_y).replace(",", ".")

    @property
    def is_working(self):
        city = self.city_items.all().first()
        if city is None:
            return False
        from django.utils import timezone
        current_time = timezone.now().hour
        return city.work_time_start.hour <= current_time <= city.work_time_end.hour

    @staticmethod
    def get_settings():
        return Settings.objects.filter(language=settings.LANGUAGE_CODE).first()

    def __str__(self):
        return str(dict(settings.LANGUAGES).get(self.language, self.language))

    def _convert_base(self, num, to_base=10, from_base=16):
        if isinstance(num, str):
            n = int(num, from_base)
        else:
            n = int(num)
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < to_base:
            return alphabet[n]
        else:
            return self._convert_base(n // to_base, to_base) + alphabet[n % to_base]

    def _darken(self, hex_color):
        o1 = self._convert_base(
            round(int(self._convert_base(hex_color[1:3])) * 0.83), 16, 10)
        if len(o1) == 1:
            o1 = "0{}".format(o1)
        o2 = self._convert_base(
            round(int(self._convert_base(hex_color[4:5])) * 0.83), 16, 10)
        if len(o2) == 1:
            o2 = "0{}".format(o2)
        o3 = self._convert_base(
            round(int(self._convert_base(hex_color[5:7])) * 0.83), 16, 10)
        if len(o3) == 1:
            o3 = "0{}".format(o3)

        return "#{}{}{}".format(o1, o2, o3)

    class Meta:
        abstract = True
        verbose_name = _('Настройки сайта')
        verbose_name_plural = _('Настройки сайта')
        ordering = ['language']


class Settings(SettingsBase):
    pass


class TypeShipping(models.Model):
    CALCULATION_TYPE = (
        ('price_out', 'Высчитывается отдельно'),
        ('price_km', 'Цена за КМ'),
        ('price_fix', 'Фиксированная цена'),
    )
    is_active = models.BooleanField('Активность', default=True)
    title = models.CharField(verbose_name="Название",
                             blank=True, default="", max_length=100)
    min_price = models.FloatField('Минимальная сумма заказа', default=0)
    show_address = models.BooleanField(
        verbose_name="Выводить поля ввода адреса", default=True)

    calculation = models.CharField(verbose_name="Способ рассчета",
                                   max_length=300, default="price_out", choices=CALCULATION_TYPE, )

    price_km = models.FloatField(
        verbose_name="Цена за КМ", default=0)

    price_fix = models.FloatField(
        verbose_name="Фиксированная цена", default=0)

    cities_free = models.TextField(verbose_name="Города с бесплатной доставкой",
                                   help_text="разделитель ;", blank=True, default="")

    cities = models.TextField(verbose_name="Доставляется только в ...(города)",
                              help_text="разделитель ;",
                              blank=True, default="")

    code = models.SlugField(
        verbose_name="Код", max_length=200, blank=True, null=True)
    display_motivational = models.BooleanField(verbose_name="Отображать мотивационное сообещение?",
                                               default=False)
    motivational_message = models.CharField(verbose_name="Мотивационное сообщение",
                                            max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_cities(self):
        return self.cities.split(";")

    def get_cities_free(self):
        return self.cities_free.split(";")

    class Meta:
        verbose_name = _('Способ доставки')
        verbose_name_plural = _('Способы доставки')
        ordering = ['id']


@receiver(pre_save, sender=TypeShipping)
def set_slug_field(sender, instance, **kwargs):
    """Сгенерировать код для типа доставки."""

    if instance.code is None or instance.code is "":
        instance.code = slugify(instance.title, allow_unicode=True)
