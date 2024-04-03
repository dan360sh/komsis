import base64
import os
import re
import shutil
import sys
import traceback
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from apps.account.models import Account
from apps.catalog import models as catalog_models
from apps.catalog.models.price import OptionPrice, ProductPrice
from apps.exchange1c.models import Settings as ExchaneSettings
from apps.feedback.models import serviceEmail
from apps.feedback.utils import template_email_message
from apps.shop import models as shop_models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from filer.models import File as FilerFile
from filer.models import Image
from lxml import etree
from slugify import slugify
from system import settings

# def decor(func):
# 	def wrapper(*args, **kwargs):
# 		try:
# 			res = func(*args, **kwargs)
# 		except:
# 			res = False
# 			traceback.print_exc()
# 		return res
# 	return wrapper

# END emailReport imports

emailNotificationsSitename = 'komsis.su'


def emailReport(func):
    def wrapper(*args, **kwargs):
        try:
            startDateTime = datetime.now()
            try:
                template_email_message('serviceEmails/_serviceTemplate_miscExchange_launch.txt',
                                       'Сайт ' + emailNotificationsSitename + ': ЗАПУСК: запуск обмена',
                                       [i.title for i in serviceEmail.objects.filter(
                                           subscription_exchange=True)],
                                       {'startTime': str(startDateTime)}, contentSubtype='plain')
            except:
                print("MAILER FAILED:")
                traceback.print_exc()

            res = func(*args, **kwargs)

            completeDateTime = datetime.now()
            try:
                template_email_message('serviceEmails/_serviceTemplate_miscExchange_complete.txt',
                                       'Сайт ' + emailNotificationsSitename + ': УСПЕХ: завершен обмен',
                                       [i.title for i in serviceEmail.objects.filter(
                                           subscription_exchange=True)],
                                       {'result': 'УСПЕХ', 'startTime': str(startDateTime),
                                        'completeTime': str(completeDateTime),
                                        'spent': str(completeDateTime - startDateTime)}, contentSubtype='plain')
            except:
                print("MAILER FAILED:")
                traceback.print_exc()
        except:
            res = False
            traceback.print_exc()
            completeDateTime = datetime.now()
            strTB = ''
            strTB += str(sys.exc_info()) + '\n'
            strTB += str(
                '\n'.join(list(traceback.format_tb(sys.exc_info()[2]))))
            try:
                template_email_message('serviceEmails/_serviceTemplate_miscExchange_complete.txt',
                                       'Сайт ' + emailNotificationsSitename + ': ОТКАЗ: завершен обмен',
                                       [i.title for i in serviceEmail.objects.filter(
                                           subscription_exchange=True)],
                                       {'result': 'ОТКАЗ', 'traceback': strTB, 'startTime': str(startDateTime),
                                        'completeTime': str(completeDateTime),
                                        'spent': str(completeDateTime - startDateTime)},
                                       contentSubtype='plain')
            except:
                print("MAILER FAILED:")
                traceback.print_exc()
        return res

    return wrapper


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


REGULAR_FOR_NAME_IMPORT_FILE = r'^import\.xml$'
REGULAR_FOR_NAME_OFFER_FILE = r'^offers\.xml$'


def generate_unique_slug(name, model):
    slug = slugify(name)
    count = 0
    while True:
        try:
            prod = model.objects.get(slug=slug)
            slug = slug + "_" + str(count)
            count += 1
        except Exception:
            break
    return slug


class Command(BaseCommand):
    SCAN_FILES = None
    FILE_PATH = settings.BASE_DIR + '/../1c/'
    CAT_PARENT = {}
    CAT_COUNT_UPDATE = 0
    CAT_COUNT_CREATE = 0
    PRODUCT_COUNT_CREATE = 0
    PRODUCT_COUNT_UPDATE = 0
    NAMESPACE = ""
    PRICES = {}
    ATTRIBUTES = {}
    STATUSES = {
        'Зарегистрирован': 'processing',
        'Зарезервирован': 'precompleted',
        'Оплачен': 'paid',
        'Собран': 'assembled',
        'Отгружен': 'shipped',
        'Отменён': 'canceled',
        'Завершен': 'completed',
    }
    DIFFEXCHANGE = False
    RECYCLER_GROUPS_IDS = set()

    # known debug flags:
    #
    # fixVeryNewDeact1 - dont import anything; collect RECYCLER_GROUPS_IDS, iterate over and deact related products
    #
    DEBUGFLAGS = []

    def add_arguments(self, parser):
        # # Positional arguments
        # parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument('--in_action', default=False)
        parser.add_argument('--filename', default="offers.xml")
        parser.add_argument('--type_i', default="import")
        parser.add_argument('--no_rewrite', default=False, action='store_true')
        parser.add_argument('--debug', nargs='+')

    # @decor
    # @emailReport
    def handle(self, *args, **options):

        self.DEBUGFLAGS = options.get('debug') or []

        document = self.is_exist_files()
        if not document:
            self.stderr.write("Файлы не найдены")
            return
        print(options)
        # return

        if options.get('filename'):
            self.import_file = options['filename']
        else:
            self.import_file = self.get_name_import_file()
        xml = os.path.join(self.FILE_PATH + self.import_file)

        document = ET.parse(xml).getroot()

        # определяем, полная ли выгрузка
        self.DIFFEXCHANGE = options.get('no_rewrite')
        marked = document.find('Каталог')
        if marked and marked.attrib.get("СодержитТолькоИзменения", False) == 'true':
            self.DIFFEXCHANGE = True
        marked = document.find('ПакетПредложений')
        if marked and marked.attrib.get("СодержитТолькоИзменения", False) == 'true':
            self.DIFFEXCHANGE = True

        # print(self.DIFFEXCHANGE)
        # return

        marked = document.find('Каталог')
        # Документ
        if document.find('Классификатор') is None and document.find('ПакетПредложений') is None and document.find(
                self.NAMESPACE + 'Документ') is None:
            self.NAMESPACE = "{urn:1C.ru:commerceml_2}"
        if not self.DIFFEXCHANGE:
            if 'fixVeryNewDeact1' not in self.DEBUGFLAGS:
                catalog_models.Product.objects.all().update(new=False)

        if document.find(self.NAMESPACE + 'ПакетПредложений'):
            if 'fixVeryNewDeact1' in self.DEBUGFLAGS:
                return
            for item in document.find(self.NAMESPACE + 'ПакетПредложений').find(self.NAMESPACE + 'ТипыЦен').findall(
                    self.NAMESPACE + "ТипЦены"):
                id = item.find(self.NAMESPACE + 'Ид').text
                title = item.find(self.NAMESPACE + 'Наименование').text
                self.PRICES[title] = id

            if not self.DIFFEXCHANGE:
                if 'fixVeryNewDeact1' not in self.DEBUGFLAGS:
                    catalog_models.Option.objects.all().delete()
            catalog_models.Product.objects.filter(
                is_clear_options=True).update(is_clear_options=False)
            for item in document.find(self.NAMESPACE + 'ПакетПредложений').find(self.NAMESPACE + 'Предложения').findall(
                    self.NAMESPACE + "Предложение"):
                self.offer_product(item)

            # Ид
            # Наименование
            # Цена Цены
            # ЦенаЗаЕдиницу
            return

        if document.findall("Карта"):
            print("ИМПОРТ ВЫГРУЗКИ БОНУСНЫХ КАРТ")
            cards = document.findall('Карта')
            for card in cards:
                self.import_bonus_card(card)
            return

        if document.findall(self.NAMESPACE + 'Документ'):
            for item in document.findall(self.NAMESPACE + 'Документ'):
                self.export_order(item)
            if not self.DIFFEXCHANGE:
                if 'fixVeryNewDeact1' not in self.DEBUGFLAGS:
                    catalog_models.Product.objects.filter(
                        count=0).update(price=0)

            return
        try:
            for item in document.find(self.NAMESPACE + 'Классификатор').find(self.NAMESPACE + 'Свойства').findall(
                    self.NAMESPACE + "Свойство"):
                if item.find(self.NAMESPACE + 'ТипЗначений') is not None and item.find(
                        self.NAMESPACE + 'ТипЗначений').text == 'Справочник':
                    item_title = item.find(
                        self.NAMESPACE + 'Наименование').text
                    item_id = item.find(self.NAMESPACE + 'Ид').text

                    if item_title == 'место хранения':
                        continue

                    if item.find(self.NAMESPACE + 'ВариантыЗначений').find(self.NAMESPACE + 'Справочник') is not None:
                        try:
                            catalog_models.AttributesGroup.objects.get(
                                unloading_id=item_id)
                        except:
                            catalog_models.AttributesGroup.objects.create(unloading_id=item_id,
                                                                          title=item_title.replace('@', ' '))
                        print(item.find(self.NAMESPACE + 'Наименование').text)
                        for _item in item.find(self.NAMESPACE + 'ВариантыЗначений').findall('Справочник'):
                            _item_id = _item.find(
                                self.NAMESPACE + 'ИдЗначения').text
                            item_name = _item.find(
                                self.NAMESPACE + 'Значение').text
                            if _item_id and item_name:
                                try:
                                    catalog_models.AttributeValue.objects.get(
                                        unloading_id=_item_id)
                                except:
                                    if not re.search(r'<.+?>', item_name):
                                        catalog_models.AttributeValue.objects.create(unloading_id=_item_id,
                                                                                     title=item_name)
        except:
            pass

        for groups in document.find(self.NAMESPACE + 'Классификатор').find(self.NAMESPACE + 'Группы').findall(
                self.NAMESPACE + "Группа"):
            self.import_group(groups)
        print("RECYCLER_GROUPS_IDS: " + str(self.RECYCLER_GROUPS_IDS))
        """try:
            catalog_models.Product.objects.all().update(new=False)
            catalog_models.Product.objects.all().update(active=False)
        except:
            print('товары отсутствуют')"""

        # if not self.DIFFEXCHANGE:
        # catalog_models.Product.objects.all().delete() # WHAT THE HELL IS THAT? DELETE PRODUCTS???

        # Словарь атрибутов "Ид:Наименование"
        for item in document.find(self.NAMESPACE + 'Классификатор').find(self.NAMESPACE + 'Свойства').findall(
                self.NAMESPACE + "Свойство"):
            self.ATTRIBUTES[item.find(
                self.NAMESPACE + 'Ид').text] = item.find(self.NAMESPACE + 'Наименование').text
        # Импорт товаров
        self.stdout.write("Импортирование товаров")
        count = 0
        products = document.find(self.NAMESPACE + 'Каталог').find(self.NAMESPACE + 'Товары').findall(
            self.NAMESPACE + "Товар")
        for product in products:
            self.import_product(product)
            count += 1
        catalog_models.Category.objects.rebuild()
        if not self.DIFFEXCHANGE:
            if 'fixVeryNewDeact1' not in self.DEBUGFLAGS:
                catalog_models.Product.objects.filter(count=0).update(price=0)

        return

    def is_exist_files(self):
        path = Path(self.FILE_PATH)
        dir_ = path.glob("*.*")
        files = [obj for obj in dir_ if obj.is_file()]
        return len(files) != 0
        # files = scandir.scandir(self.FILE_PATH)
        # self.SCAN_FILES = files
        # b = False
        # for s in files:
        #     b = True
        #     break
        # return b

    def export_order(self, et_order):
        try:
            document_order_items = ""
            order = shop_models.Order.objects.get(
                id=et_order.find(self.NAMESPACE + "Номер").text)
            for i in et_order.find(self.NAMESPACE + "ЗначенияРеквизитов").findall(self.NAMESPACE + "ЗначениеРеквизита"):
                if i.find(self.NAMESPACE + "Наименование").text == "Статус заказа":
                    if i.find(self.NAMESPACE + "Значение").text:
                        print(self.STATUSES[i.find(
                            self.NAMESPACE + "Значение").text])
                        order.status = self.STATUSES[i.find(
                            self.NAMESPACE + "Значение").text]
                        order.save()

            # for item in order.order_items.all():
            #	 print(item)
            #
            # order.changed = True
            local_product_dict = {}
            for i in et_order.find(self.NAMESPACE + "Товары").findall(self.NAMESPACE + "Товар"):
                local_product = {
                    "count": i.find(self.NAMESPACE + u"Количество").text,
                    "price": i.find(self.NAMESPACE + "ЦенаЗаЕдиницу").text,
                }
                local_product_dict[i.find(
                    self.NAMESPACE + "Ид").text] = local_product
            order_items = order.order_items.all()

            for key, value in local_product_dict.items():
                try:
                    order_items.get(product__unloading_id=key)
                except ObjectDoesNotExist:
                    try:
                        product = catalog_models.Product.objects.get(
                            unloading_id)
                        shop_models.OrderItem.create(order=order, product=product, count=value['color'],
                                                     total=value['price'])
                        order.changed = True
                        order.save()
                    except:
                        print('Продукта нет')
                        continue
                except:
                    print('найдено 2 объекта')

            for item in order.order_items.all():
                if not item.product.unloading_id in local_product_dict:
                    item.delete()
                    order.changed = True
                    order.save()
            print(order.changed)

        except ObjectDoesNotExist:
            print("заказ не существует")

    def import_group(self, group, parent=None, recyclerHier=None):
        try:
            id_1c = group.find(self.NAMESPACE + "Ид").text.strip(" \n\t")
            category_name = group.find(
                self.NAMESPACE + "Наименование").text.strip(" \n\t")
        except:
            self.stderr.write("Проблема с информацией в категории")
            traceback.print_exc()
            return

        # BEGIN 200508: VERY NEW DEACTIVATION LOGIC
        # based on product membership in a groups hierarchy of "я ЗАКАЗНОЙ ТОВАР ..." (82f466e6-e06e-11dd-97c1-0016e65f1671).
        # in a full exchange mode those products are completely ignored, in diff exchange mode -- deactivated

        childs = group.find(self.NAMESPACE + "Группы")
        if id_1c == '82f466e6-e06e-11dd-97c1-0016e65f1671' or recyclerHier:
            self.RECYCLER_GROUPS_IDS.add(id_1c)
            if childs:
                for item in childs.findall(self.NAMESPACE + "Группа"):
                    self.import_group(item, parent=None, recyclerHier=True)
            return

        if 'fixVeryNewDeact1' in self.DEBUGFLAGS:
            return

        # END 200508: VERY NEW DEACTIVATION LOGIC

        if category_name != 'Интернет-магазин':
            print(id_1c, category_name, parent)
            slug = slugify(category_name) if not parent else slugify(
                category_name + parent.title)
            # Создание или обновление категории товаров
            fields = ({
                'unloading_id': id_1c,
                'title': category_name,
                'slug': slug,
                'parent': parent
            })
            if parent:
                category, created = catalog_models.Category.objects \
                    .update_or_create(unloading_id=id_1c, defaults=fields)
            else:
                category, created = catalog_models.Category.objects \
                    .update_or_create(unloading_id=id_1c, defaults=fields)

            # childs = group.find(self.NAMESPACE + "Группы") # moved upwards
            if childs is not None:
                for item in childs.findall(self.NAMESPACE + "Группа"):
                    self.import_group(item, category)

    def offer_product(self, product):
        # active = True # do not activate products that are otherwise deactivated
        active = None
        id_1c = product.find(self.NAMESPACE + "Ид").text.strip(" \n\t")
        try:
            status = product.find(
                self.NAMESPACE + "Статус").text.strip(" \n\t")
        except AttributeError as e:
            status = ''
            print('Ошибка статуса', str(e))

        if id_1c.find("#") > -1:
            parent_id, id_1c = id_1c.split("#")
            try:
                parent = catalog_models.Product.objects.get(
                    unloading_id=parent_id)

            except:
                print('родитель не найден')
                parent = None
        else:
            parent = None

        print(status)
        if status == 'Удален':
            active = False
            print('*' * 100)

        print(id_1c)

        try:
            product_name = product.find(
                self.NAMESPACE + "Наименование").text.strip(" \t\n")
        except Exception as e:
            product_name = ''
            print('Имя продукта', str(e))

        try:
            product_name = product.find(
                self.NAMESPACE + "Характеристика").text.strip(" \t\n")
        except Exception as e:
            print("net product_option_title")
            print('Ошибка: Имя продукта Характеристика', str(e))

        step = 1
        try:
            step = product.find(
                self.NAMESPACE + "Кратность").text.strip(" \t\n")
        except Exception as e:
            print("net step offers")
            print('Ошибка: Нет кратности', str(e), product_name)
        # импорт цены
        prices = {}
        product_price = 0
        if product.find(self.NAMESPACE + "Цены"):
            for price in product.find(self.NAMESPACE + "Цены").getchildren():
                product_price_id = price.find(
                    self.NAMESPACE + 'ИдТипаЦены').text
                product_price = price.find(
                    self.NAMESPACE + 'ЦенаЗаЕдиницу').text
                prices[product_price_id] = product_price

        if prices:
            product_price = list(prices.values())[0]

        print(product_price)

        try:
            count = float(product.find(self.NAMESPACE + u"Количество").text)
        except AttributeError:
            count = 0

        try:
            tags = product.find(self.NAMESPACE + "Тэги").text.strip(" \t\n")
        except:
            tags = ''

        fields = ({
            #	'active': active,
            'title': product_name,
            'price': product_price,
            'count': count,
            'product': parent,
            'step': step,
        })

        if active is not None:  # expected False when deactivated via Удален element,
            # None otherwise. no ultimate reactivation should be done in this method.
            fields['active'] = active

        storages = []
        try:
            for xml_storage in product.find(self.NAMESPACE + 'Склады').findall(self.NAMESPACE + 'Склад'):
                storage_title = xml_storage.find(
                    self.NAMESPACE + 'Представление').text.strip(" \t\n")
                storage_count = xml_storage.find(self.NAMESPACE + 'Количество')
                if storage_count is None:
                    storage_count = 0
                else:
                    storage_count = storage_count.text.strip(" \t\n")
                storage, created = catalog_models.ProductStorage.objects.get_or_create(
                    upload_title=storage_title)
                storages.append(
                    {'storage': storage, 'count': float(storage_count)})
        except Exception as e:
            print('Ошибка: НЕТ СКЛАДА ', str(e), product_name)
        try:
            prod = catalog_models.Product.objects.get(unloading_id=id_1c)
            if prod.is_clear_options is False:
                prod.options.all().delete()
                prod.is_clear_options = True
                prod.save(update_fields=['is_clear_options'])
            prod.title_upper = tags

            # Проверка наличия в выгрузке нового типа цен или изменения
            # наименования для уже существующего
            for type_price_title in self.PRICES:
                type_price_id = self.PRICES[type_price_title]
                try:
                    type_price = catalog_models.PriceType.objects.get(
                        pk=type_price_id)
                    type_price.title = type_price_title
                except catalog_models.PriceType.DoesNotExist:
                    type_price = catalog_models.PriceType.objects.create(
                        pk=type_price_id,
                        title=type_price_title
                    )
                type_price.save()

            # ТИПЫ ЦЕН
            data_prices = prices.copy()
            # Выгрузка всех цен товара
            for price_key in data_prices:
                type_price = catalog_models.PriceType.objects.get(pk=price_key)
                try:
                    product_price = catalog_models.ProductPrice.objects.get(
                        type=type_price,
                        product=prod
                    )
                except ProductPrice.DoesNotExist:
                    product_price = catalog_models.ProductPrice.objects.create(
                        type=type_price,
                        product=prod
                    )
                value = float(prices[price_key])
                if value <= 0:
                    value = 0
                print(
                    f"Товар: {product_price.product.title}\nТип цены: {type_price}\nЗначение цены: {value}")
                # Если пришла цена меньше, чем цена товара на момент выгрузки
                # В поле "Старая цена" поставить текущую цену
                if product_price.value > value:
                    product_price.old_value = product_price.value
                # Если текущая цена товара меньше пришедшей
                # Выставить 0 в поле "Старая цена"
                if product_price.value < value:
                    product_price.old_value = 0
                # В поле "Цена" выставляем пришедшую цену
                product_price.value = value
                product_price.save()

            # Получаем атрибут товара ТипЦены
            price_type = prod.product_attrbutes.filter(
                group__title='ТипЦены').first()
            price_type_title = 'Опт'
            # Получаем название Типа цены
            if price_type and price_type.value:
                price_type_title = price_type.value.title
            # в словаре цен ищем айди цены по названию
            price_type_id = self.PRICES.get(
                price_type_title, 'a6bfe5d2-ccce-11dd-8d29-001fc6b4b87e')
            # Берем нужную цену из спарсенных цен, если ничего не найдено оставляем старую
            product_price = prices.get(price_type_id, product_price)
            # prod.active = True
            if active is not None:
                prod.active = active

            if float(product_price) <= 0:
                product_price = 0
            if prod.price > float(product_price):
                prod.old_price = prod.price
                print("old_price" * 10)
                prod.sale = True
            prod.step = float(step)
            prod.price = float(product_price)
            prod.tech_price = float(product_price)
            try:
                prod.count = float(product.find(
                    self.NAMESPACE + u"Количество").text)
            except Exception as e:
                prod.count = 0
                print('Ошибка: Нет количества', str(e), prod)
            # сохраняем общее количество
            if storages:
                prod.count = sum(storage.get('count', 0)
                                 for storage in storages)
                print('Количество товара на всех складах', prod.count)
            prod.save()
            for storage in storages:
                product_count, created = catalog_models.ProductStorageCount.objects \
                    .update_or_create(product=prod, storage=storage['storage'],
                                      defaults={'count': storage.get('count', 0)})
        except Exception as e:
            print('Ошибка продукта', str(e), product_name)

        if parent:
            price_type = parent.product_attrbutes.filter(
                group__title='ТипЦены').first()
            price_type_title = 'Опт'
            # Получаем название Типа цены
            if price_type and price_type.value:
                price_type_title = price_type.value.title
            # в словаре цен ищем айди цены по названию
            price_type_id = self.PRICES.get(
                price_type_title, 'a6bfe5d2-ccce-11dd-8d29-001fc6b4b87e')
            # Берем нужную цену из спарсенных цен, если ничего не найдено оставляем старую
            product_price = prices.get(
                'a6bfe5d2-ccce-11dd-8d29-001fc6b4b87e', product_price)
            fields['price'] = product_price
        opt, created = catalog_models.Option.objects.update_or_create(
            unloading_id=id_1c, defaults=fields)
        if parent:
            for storage in storages:
                print('STORAGE OPTION', storage)
                product_count, created = catalog_models.ProductStorageCount.objects \
                    .update_or_create(option=opt, storage=storage['storage'],
                                      defaults={
                                          'count': storage.get('count', 0)}
                                      )
            # Выгрузка всех цен опции
            data_prices = prices.copy()
            for price_key in data_prices:
                type_price = catalog_models.PriceType.objects.get(pk=price_key)
                try:
                    option_price = catalog_models.OptionPrice.objects.get(
                        type=type_price,
                        option=opt
                    )
                except OptionPrice.DoesNotExist:
                    option_price = catalog_models.OptionPrice.objects.create(
                        type=type_price,
                        option=opt
                    )
                value = float(data_prices[price_key])
                if value <= 0:
                    value = 0
                print(
                    f"Опция: {option_price.option.title}\nТип цены: {type_price}\nЗначение цены: {value}")
                # Если пришла цена меньше, чем цена опции на момент выгрузки
                # В поле "Старая цена" поставить текущую цену
                if option_price.value > value:
                    option_price.old_value = option_price.value
                # Если текущая цена опции меньше пришедшей
                # Выставить 0 в поле "Старая цена"
                if option_price.value < value:
                    option_price.old_value = 0
                # В поле "Цена" выставляем пришедшую цену
                option_price.value = value
                option_price.save()

        return

    def import_product(self, product):
        product_xml = product
        # BEGIN 200429: deactivating/skipping products w/ "ВыгружатьНаСайт" property set to false
        SKIPPRODUCT = False
        try:
            attrs = product_xml.find(self.NAMESPACE + "ЗначенияСвойств") \
                .findall(self.NAMESPACE + "ЗначенияСвойства")
        except Exception:
            return
        for attr in attrs:
            try:
                attribute_id = attr.find(self.NAMESPACE + "Ид") \
                    .text.strip(" \t\n")
                attribute_name = self.ATTRIBUTES[attribute_id]
            # attribute_name = str(attribute_name).replace('@', ' ')
            except:
                continue

            try:
                attribute_value = attr.find(self.NAMESPACE + "Значение") \
                    .text.strip(" \t\n")
            except:
                continue
            if attribute_name and attribute_name == 'ВыгружатьНаСайт' and attribute_value and attribute_value.lower() == 'false':
                print("----200429 SKIPPING PRODUCT by attribute ", product)
                SKIPPRODUCT = True
        # END 200429: deactivating/skipping products w/ "ВыгружатьНаСайт" property set to false

        active = True
        try:
            id_1c = product.find(self.NAMESPACE + "Ид").text.strip(" \n\t")
            group = product.find(
                self.NAMESPACE + "Группы").find(self.NAMESPACE + "Ид").text.strip(" \t\n")

            # 200429 no more Статус=Удален here
            # 200512 oops, it's still there, in offers.
            try:
                status = product.find(
                    self.NAMESPACE + "Статус").text.strip(" \t\n")
            except AttributeError:
                status = ''

            if status and status == 'Удален':
                active = False
                print('*' * 100)

            # BEGIN 200508: VERY NEW DEACTIVATION LOGIC
            if group and group in self.RECYCLER_GROUPS_IDS:
                if self.DIFFEXCHANGE:
                    print(
                        "--- 200508: VERY NEW DEACTIVATION LOGIC TRIGGERED: DIFF MODE")
                    self.deactOrDeleteProduct(id_1c)
                    return
                else:
                    print(
                        "--- 200508: VERY NEW DEACTIVATION LOGIC TRIGGERED: FULL MODE")
                    # we shouldn't discriminate this until deact logic is stabilized
                    self.deactOrDeleteProduct(id_1c)
                    return
            # END 200508: VERY NEW DEACTIVATION LOGIC

            # BEGIN 200429: deactivating/skipping products w/ "ВыгружатьНаСайт" property set to false
            if SKIPPRODUCT:
                print("--- 200429: NEW DEACTIVATION LOGIC TRIGGERED")
                self.deactOrDeleteProduct(id_1c)
                return
            # END 200429: deactivating/skipping products w/ "ВыгружатьНаСайт" property set to false

            if 'fixVeryNewDeact1' in self.DEBUGFLAGS:
                return

            cat = catalog_models.Category.objects.get(unloading_id=group)

            product_name = product.find(
                self.NAMESPACE + "Наименование").text.strip(" \t\n")  # .replace("  "," ").replace("   "," ")
            product_unit = product.find(
                self.NAMESPACE + "БазоваяЕдиница").text.strip(" \t\n")
            # product_price = product.find(
            #	 self.NAMESPACE + "Цена2").text.strip(" \n\t")
            # product_wholesale_price = product.find(
            #	 self.NAMESPACE + "Цена").text.strip(" \n\t")
            # product_count = product.find(
            #	 self.NAMESPACE + "Остаток").text.strip(" \n\t")
            try:
                product_desc = product.find(
                    self.NAMESPACE + "Описание").text.strip(" \t\n")
            except AttributeError:
                product_desc = ""
            try:
                product_code = product.find(
                    self.NAMESPACE + "Артикул").text.strip(" \n\t")
            except AttributeError:
                product_code = ""
            try:
                product_barcode = product.find(
                    self.NAMESPACE + "Штрихкод").text.strip(" \n\t")
            except AttributeError:
                product_barcode = ""

            try:
                print("---------- Картинки -------- ")
                image_path_list = product.findall(self.NAMESPACE + 'Картинка')
            except AttributeError:
                image_path_list = None
            print("-" * 50, image_path_list)

            try:
                file_path = product.find(self.NAMESPACE + 'ЗначенияРеквизитов'). \
                    find(self.NAMESPACE + 'ЗначениеРеквизита')
                file_path = file_path.find(
                    self.NAMESPACE + 'Значение').text.strip(" \n\t")
                if file_path.split(".")[-1] != "pdf":
                    raise Exception("Неверный формат файла")
            except Exception:
                file_path = None

        except Exception:
            self.stderr.write("Проблема с информацией в товаре")
            traceback.print_exc()
            return
        print(id_1c, product_name, group)
        # print('путь'+ image_path)

        slug = slugify(
            product_name + product_code) if product_code else slugify(product_name + cat.title)
        full_name = product_name.upper()
        try:
            requisites = product.find(self.NAMESPACE + 'ЗначенияРеквизитов').findall(
                self.NAMESPACE + 'ЗначениеРеквизита')
            for requisit in requisites:
                if requisit.find(self.NAMESPACE + 'Наименование').text.strip(" \t\n") == 'Полное наименование':
                    full_name = requisit.find(
                        self.NAMESPACE + 'Значение').text.strip(" \t\n")
        except:
            pass

        # Создание и обновление категории
        fields = {
            'unloading_id': id_1c,
            'code': product_code,
            'title': product_name,
            'title_upper': full_name,
            'slug': slug,
            'category': cat,
            # 'price': int(product_price),
            # 'wholesale_price': int(product_wholesale_price),
            'old_price': 0,
            # 'count': int(product_count),
            'description': product_desc,
            'description_upper': product_desc.upper(),
            # 'hit': False,
            # 'new': False,
            'sale': False,
            'active': active,
            'unit': product_unit,
        }
        try:
            product, created = catalog_models.Product.objects.update_or_create(
                unloading_id=id_1c, defaults=fields)
            if created:
                product.new = True
                product.save()
        except IntegrityError:
            # while 1:
            fields['slug'] += "1"
            try:
                product, created = catalog_models.Product.objects.update_or_create(
                    unloading_id=id_1c, defaults=fields)
            # break
            except:
                print(id_1c)
                return
        self.set_attributes(product_xml, product)
        product.active = active
        product.save()
        if image_path_list:
            self.set_thumbnail(product, image_path_list[0].text.strip(" \n\t"))

        try:
            if len(image_path_list) >= 1:
                for image in image_path_list[1:]:
                    self.set_gallery_image(product, image.text.strip(" \n\t"))
        except:
            pass

        try:
            if file_path:
                self.set_file(product, file_path)
        except:
            raise e

    def set_attributes(self, product_xml, product):
        product.product_attrbutes.all().delete()
        try:
            attrs = product_xml.find(self.NAMESPACE + "ЗначенияСвойств") \
                .findall(self.NAMESPACE + "ЗначенияСвойства")
        except Exception:
            return
        print('set_attrs', attrs)
        for attr in attrs:
            try:
                attribute_id = attr.find(self.NAMESPACE + "Ид") \
                    .text.strip(" \t\n")
                attribute_name = self.ATTRIBUTES[attribute_id]
            # attribute_name = str(attribute_name).replace('@', ' ')
            except:
                continue

            try:
                attribute_value = attr.find(self.NAMESPACE + "Значение") \
                    .text.strip(" \t\n")
            except:
                continue
            if attribute_name and attribute_value:
                if attribute_name == 'Направление':
                    try:
                        direction = catalog_models.Direction.objects \
                            .get(title_original=attribute_value)
                    except ObjectDoesNotExist:
                        direction = catalog_models.Direction.objects \
                            .create(title=attribute_value,
                                    title_original=attribute_value)
                    product.directions.add(direction)
                    continue
                if attribute_name == 'Кратность':
                    product.step = float(attribute_value)
                    product.save()
                    continue
                if attribute_name == 'Производитель':
                    try:
                        brand = catalog_models.Brand.objects \
                            .get(slug=slugify(attribute_value))
                    except ObjectDoesNotExist:
                        brand = catalog_models.Brand.objects \
                            .create(title=attribute_value,
                                    slug=slugify(attribute_value))
                    product.brand = brand
                    product.save()
                    continue
                # if attribute_name == 'Распродажа' and attribute_value == 'true':
                if attribute_name == 'Распродажа':
                    product.sale = True if attribute_value.lower() == 'true' else False
                    product.save(update_fields=['sale'])
                    continue
                if attribute_name == 'ВыгружатьЦену' and attribute_value == '0':
                    product.price = 0
                    product.tech_price = product.price
                    product.save(update_fields=['price', 'tech_price'])
                    # у товара с атрибутами "распродажа" и "выгружать цену=0"
                    # Если остаток > 0 то цену показыать
                    if product.sale and product.price == 0 and product.count > 0:
                        product.price = product.tech_price
                        product.save()
                    continue
                if attribute_name == 'Приоритет':
                    try:
                        sort = int(attribute_value)
                    except:
                        sort = None
                    if sort > 999999999:
                        sort = None
                    product.sort = sort
                    product.save(update_fields=['sort'])
                if attribute_name == 'ВыгружатьЦену' and attribute_value == '1':
                    continue
                # else:
                #	 continue
                if attribute_name == 'Аналоги' \
                        or attribute_name == 'место хранения':
                    continue
                if attribute_name == 'объем':
                    attribute_name = 'Объем'
                group, created = catalog_models.AttributesGroup \
                    .objects.update_or_create(title=attribute_name.replace('@', ' '))
                value, created = catalog_models.AttributeValue \
                    .objects.update_or_create(title=attribute_value)
                catalog_models.Attribute.objects.update_or_create(
                    product=product, value=value, group=group)

    def set_thumbnail(self, instance, image_path):
        if image_path:
            image_media_path = os.path.join(
                settings.MEDIA_ROOT, 'products', image_path)
            # image_1c_path = os.path.join(self.FILE_PATH, image_path)
            thumbnail = self.create_image(image_media_path, image_path)
            if not thumbnail:
                return None
            instance.thumbnail = thumbnail
            instance.save()

    def set_file(self, instance, file_path):
        print(instance, file_path)
        if file_path:
            file_1c_path = os.path.join(self.FILE_PATH, file_path)
            file = self.create_file(file_1c_path, file_path)
            print("ffff", file, "ffff")
            a = '<a href="{url}">Дополнительная информация</a>'.format(
                url=file.url)
            if instance.description and instance.description.find("Дополнительная информация") < 0:
                instance.description = a + instance.description
                instance.save()
            elif not instance.description:
                instance.description = a
                instance.save()

    def set_gallery_image(self, product, image):
        product.product_gallery.all().delete()
        # name = image[image.rfind('/') + 1:]
        url = image
        image_media_path = os.path.join(settings.MEDIA_ROOT, 'products', url)
        # if not os.path.isfile(image_media_path): return
        image = self.create_image(image_media_path, url)
        if not image:
            return None
        catalog_models.ProductGallery.objects.create(
            product=product, photo=image)
        return image

    def get_image_base64(self, image_base64, product):
        path = os.path.join(settings.MEDIA_ROOT, 'products')
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        path = os.path.join(path, product.slug + '.png')
        name = product.slug + '.png'
        self.decb64img(image_base64, path)
        return path, name

    def create_image(self, path, name):
        if not os.path.isfile(path):
            return None
        with open(path, 'rb') as full_path:
            file_obj = File(full_path, name=name)
            user = User.objects.get(username='Admin')
            fields = ({'original_filename': name,
                      'owner': user, 'file': file_obj})
            try:
                image = Image.objects.update(
                    original_filename=name, defaults=fields)
            except:
                image = Image.objects.create(**fields)

            full_path.close()
            return image

    def create_file(self, path, name):
        with open(path, 'rb') as full_path:
            file_obj = File(full_path, name=name)
            user = User.objects.get(username='Admin')
            fields = ({'original_filename': name,
                      'owner': user, 'file': file_obj})

            try:
                image = FilerFile.objects.get(original_filename=name)
                print("-" * 62, "Picture already exists")
            except:
                image = FilerFile.objects.create(**fields)
            print("--------------------------------------------------------------{}   {}	{}".format(fields, name, path))

            print(
                "{}--------------------------------------------------------------".format(image))
            return image

    def decb64img(self, str, path):
        with open(path, 'wb') as file_obj:
            file_obj.write(base64.b64decode(str))
            file_obj.close()
            return path

    def deactOrDeleteProduct(self, id_1c):
        product = catalog_models.Product.objects.filter(unloading_id=id_1c)
        if product.count():
            p = product[0]
            try:
                print("---- SKIPPING PRODUCT: DEACT: ", id_1c)
                p.active = False
                p.save()
            except:
                print("---- SKIPPING PRODUCT: DEL: ", id_1c)
                p.delete()
        else:
            print("---- SKIPPING PRODUCT: NOTFOUND: ", id_1c)

    def import_bonus_card(self, card):
        if not card:
            return None

        fields_block = card.find('ЗначенияРеквизитов')
        card_id = ""
        owner_inn = ""
        owner_fullname = ""
        owner_phone = ""
        owner_email = ""
        card_balance = float(0)

        for field in fields_block.findall("ЗначениеРеквизита"):
            field_name = field.find("Наименование").text
            field_value = field.find("Значение").text
            if field_name == "НомерКарты":
                card_id = field_value
                continue
            if field_name == "КонтрагентИНН":
                owner_inn = field_value
                continue
            if field_name == "КонтрагентНаименование":
                owner_fullname = field_value
                continue
            if field_name == "Телефон":
                owner_phone = field_value.replace(' ', '')
                continue
            if field_name == "Остаток":
                card_balance = float(field_value)
                continue
            if field_name == "email":
                owner_email = field_value
                continue

        # Отделяем принты друг от друга
        SEPARATOR = "=================================================="
        print(SEPARATOR)

        message_to_print = f"""
        Номер карты: {card_id}
        ИНН: {owner_inn}
        ФИО: {owner_fullname}
        Телефон: {owner_phone}
        Email: {owner_email}
        Баланс карты: {card_balance}
        """
        print(message_to_print)

        # Если пришедший баланс карты == 0
        # скипаем карту
        if card_balance == 0:
            message_to_print = f"""
            Количесто баллов = 0, пропуск
            """
            print(message_to_print)
            return

        if owner_fullname == "":
            message_to_print = f"""
            Имя пользователя пустое, пропуск
            """
            return

        if owner_phone == "":
            message_to_print = f"""
            Номер телефона пуст, пропуск
            """
            return

        # Берем номер телефона без 8 или 7
        clear_phone = Account.get_valid_phone(owner_phone)

        account = Account.get_account(clear_phone, owner_inn, owner_email)
        # Если по переданным полям не был найден аккаунт
        if account is None:
            message_to_print = f"""
            Аккаунт не найден
            ФИО: {owner_fullname}
            ИНН: {owner_inn}
            Телефон: {owner_phone}
            """
            print(message_to_print)
            return

        message_to_print = f"""
        Аккаунт: {account.full_name}
        ИНН: {account.company_inn}
        Телефон: {account.phone}
        Кол-во баллов, которое было на аккаунте: {account.points_total}
        Кол-во баллов к начислению: {card_balance}
        """
        print(message_to_print)
        # Найденому аккаунту сохраняем
        # пришедшее кол-во бонусов
        account.points_total = card_balance
        account.bonus_card_id = card_id
        account.save()
