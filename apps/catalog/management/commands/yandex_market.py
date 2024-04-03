import os

from datetime import datetime

from lxml import etree
from lxml.builder import E

from django.core.management.base import BaseCommand
from system import settings
from apps.catalog import models as catalog_models
from apps.configuration.models import TypeShipping


FOLDER_PATH = settings.MEDIA_ROOT + '/feed'
FILE_PATH = FOLDER_PATH + '/catalog.yml'
SITE_URL = "https://komsis.su"


# from apps.configuration import Settings as SiteSettings
# site_settings = SiteSettings.objects.first()
# if not site_settings:
#     site_settings = SiteSettings()

class SiteSettings():
    def __init__(self):
        super(SiteSettings, self).__init__()
        self.name = "Комсис"
        self.company = "Комсис"


site_settings = SiteSettings()

EXPORT_SETTINGS = {
    'plus-brand': False,  # Добавляет к названию товара бренд
    'delivery': True,  # Включить доставку в выгрузку
    # Автоматическое отслеживание изменения цен(яндекс сам ставит скидки)
    'auto-discount': False,
}


def get_or_create_folder():
    if os.path.exists(FOLDER_PATH):
        return True
    try:
        os.mkdir(FOLDER_PATH)
    except OSError:
        print("Creating dir '%s' failed" % FOLDER_PATH)
        return False
    else:
        print("Success created dir '%s'" % FOLDER_PATH)
        return True


# Не учитываются дочерние/вариативные товары
# т.к. в документации яндекса написано что в группы объединяются
# только товары определенных категорий (параметр group_id)
# https://yandex.ru/support/partnermarket/offers.html
def get_products():
    return (catalog_models.Product
            .objects
            .select_related('brand', 'category')
            .filter(
                active=True,
                parent=None,
                count__gt=0,
                price__gt=0)
            )


def get_categories():
    return catalog_models.Category.objects.filter(active=True)


class Command(BaseCommand):
    def handle(*args, **options):
        generate_yml()


def generate_yml():
    if not get_or_create_folder():
        return
    print("Start xml generation")
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    catalog_xml = etree.Element('yml_catalog', date=date_now)

    doc = etree.ElementTree(catalog_xml)

    catalog_xml.append(generate_shop())

    print("Finish xml generation")
    doc.write(FILE_PATH, pretty_print=True,
              xml_declaration=True, encoding='UTF-8')


def generate_shop():
    shop_xml = E.shop()
    etree.SubElement(shop_xml, "name").text = site_settings.name

    # etree.SubElement(shop_xml, "company").text = site_settings.company

    etree.SubElement(shop_xml, "url").text = SITE_URL

    # currencies = etree.SubElement(shop_xml, "currencies")
    # etree.SubElement(currencies, "currency", id="RUR", rate="1")

    # # categories
    # print("Generate categories")
    # categories = etree.Element('categories')
    # for category in get_categories():
    #     print("*", category.title)
    #     categories.append(generate_category(category))
    # shop_xml.append(categories)
    # print("Categories generated")

    # # delivery options from site settings
    # if EXPORT_SETTINGS['delivery']:
    #     print("Generate shippings")
    #     delivery_xml = generate_delivery()
    #     if delivery_xml is not None:
    #         shop_xml.append(delivery_xml)
    #         print("shippings generated")
    #     else:
    #         print("shippings undefined")
    #     pickup_xml = generate_pickup()
    #     if pickup_xml is not None:
    #         shop_xml.append(pickup_xml)
    #         print("pickup added")

    # # on/off autocalculation discount
    # if EXPORT_SETTINGS['auto-discount']:
    #     etree.SubElement(shop_xml).text = 'yes'

    # offers
    print("Generate offers")
    offers = etree.Element('offers')
    for product in get_products():
        print("**", product.title)
        offers.append(generate_product(product))
    shop_xml.append(offers)
    print("Offers generated")

    return shop_xml


def generate_category(category):
    kwargs = {"id": str(category.id)}
    if category.parent_id:
        kwargs['parentId'] = str(category.parent_id)
    category_xml = etree.Element("category", **kwargs)
    category_xml.text = category.title
    return category_xml


def generate_delivery():
    shippings = TypeShipping.objects.filter(calculation='price_fix')\
                    .exclude(title__icontains='Самовывоз')
    if not shippings:
        return None
    delivery_xml = etree.Element("delivery-options")
    for ship in shippings:
        etree.SubElement(delivery_xml, 'option',
                         cost=str(int(ship.price_fix)))
    return delivery_xml


def generate_pickup():
    pickup = TypeShipping.objects.filter(calculation='price_fix',
                                         title__icontains='Самовывоз')
    if not pickup:
        return None
    pickup = pickup[0]
    pickup_xml = etree.Element("pickup-options")
    etree.SubElement(pickup_xml, 'option', cost=str(int(pickup.price_fix)))
    # option_xml.text = pickup.title
    return pickup_xml


def generate_product(product):

    # available = 'true' if product.count > 0 else 'false'
    xml = etree.Element('offer', id=str(product.id))#, available=available)

    etree.SubElement(xml, 'name').text = product.title
    # if EXPORT_SETTINGS['plus-brand'] and product.brand:
    #     name.text = "{} {}".format(product.title, product.brand.title)
    # else:
    #     name.text = product.title
    # if product.brand:
    #     etree.SubElement(xml, 'vendor').text = product.brand.title

    if product.price:
        etree.SubElement(xml, 'price').text = str(product.price)

    url = etree.SubElement(xml, 'url')
    url.text = SITE_URL + product.get_absolute_url()

    # if product.old_price > 0 and product.old_price > product.price:
    #     etree.SubElement(xml, 'oldprice').text = str(product.old_price)

    # etree.SubElement(xml, 'currencyId').text = 'RUR'

    etree.SubElement(xml, 'categoryId').text = str(product.category.title)

    if product.thumbnail:
        picture_xml = etree.SubElement(xml, 'picture')
        picture_xml.text = SITE_URL + product.thumbnail.url

    for pic in product.product_gallery.all():
        picture_xml = etree.SubElement(xml, 'picture')
        picture_xml.text = SITE_URL + pic.photo.url

    if product.description:
        description = etree.SubElement(xml, 'description')
        description.text = etree.CDATA(product.description)

    # # condition sale, example: 'Минимальный заказ — 4 пачки.'
    # if product.sales_notes:
    #     sales_notes_xml = etree.SubElement(xml, 'sales_notes')
    #     sales_notes_xml.text = product.sales_notes[:50]

    # params_xml = etree.SubElement(xml, 'params')

    # params = product.product_attrbutes\
    #                 .select_related('group', 'value').all()
    # for param in params:
    #     if param.group.title and param.value.title:
    #         param_xml = etree.SubElement(xml, 'param',
    #                                      name=param.group.title)
    #         param_xml.text = param.value.title

    # colors = product.colors.select_related('value').all()
    # for color in colors:
    #     if color.value and color.value.title:
    #         param_xml = etree.SubElement(xml, 'param', name='Цвет')
    #         param_xml.text = color.value.title

    return xml
