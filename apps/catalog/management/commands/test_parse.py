import base64
import os
import re
import shutil
import traceback
from xml.etree import ElementTree as ET

import scandir
from apps.catalog import models as catalog_models
from apps.exchange1c.models import Settings as ExchaneSettings
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


class Command(BaseCommand):
    xml = '/var/www/komsis.su/1c/test_offers.xml'
    NAMESPACE = ''
    PRICES = {}
    ATTRIBUTES = {}
    FILE_PATH = settings.BASE_DIR + '/../1c/'

    def handle(self, *args, **options):
        document = ET.parse(self.xml).getroot()
        # try:
        for item in document.find(self.NAMESPACE + 'ПакетПредложений').find(self.NAMESPACE + 'ТипыЦен').findall(
                self.NAMESPACE + "ТипЦены"):
            id = item.find(self.NAMESPACE + 'Ид').text
            title = item.find(self.NAMESPACE + 'Наименование').text
            self.PRICES[title] = id
            # Get or create price type by id and title
        i = 0
        for item in document.find(self.NAMESPACE + 'ПакетПредложений').find(self.NAMESPACE + 'Предложения').findall(
                self.NAMESPACE + "Предложение")[i:]:
            i += 1
            self.offer_product(item)
        # except:
        #     pass
        try:
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
                print(count)
                count += 1
        except:
            pass

    def offer_product(self, product):
        # active = True # do not activate products that are otherwise deactivated
        active = None
        id_1c = product.find(self.NAMESPACE + "Ид").text.strip(" \n\t")
        try:
            status = product.find(
                self.NAMESPACE + "Статус").text.strip(" \n\t")
        except AttributeError:
            status = ''

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
            print('Ошибка: ', str(e))
            product_name = ''

        try:
            product_name = product.find(
                self.NAMESPACE + "Характеристика").text.strip(" \t\n")
        except Exception as e:
            print('Ошибка: ', str(e))
            print("net product_option_title")

        step = 1
        try:
            step = product.find(
                self.NAMESPACE + "Кратность").text.strip(" \t\n")
        except Exception as e:
            print('Ошибка: ', str(e))
            print("net step offers")
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
        except Exception as e:
            print('Ошибка: ', str(e))
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
            print('Ошибка: ', str(e))
        try:
            prod = catalog_models.Product.objects.get(unloading_id=id_1c)
            if prod.is_clear_options is False:
                prod.options.all().delete()
                prod.is_clear_options = True
                prod.save(update_fields=['is_clear_options'])
            prod.title_upper = tags
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
            try:
                prod.count = float(product.find(
                    self.NAMESPACE + u"Количество").text)
            except Exception as e:
                print('Ошибка: ', str(e))
                prod.count = 0
            if prod.count == 0:
                product_price = 0
            # print("количество", prod.count)
            prod.save()
            for storage in storages:
                product_count, created = catalog_models.ProductStorageCount.objects \
                    .update_or_create(product=prod, storage=storage['storage'],
                                      defaults={'count': storage.get('count', 0)})
        except Exception as e:
            print('Ошибка: ', str(e), 'Опция? родитель - ', parent)
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
            product_price = prices.get(price_type_id, product_price)
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
        return

    def set_attributes(self, product_xml, product):
        # product.product_attrbutes.all().delete()
        try:
            attrs = product_xml.find(self.NAMESPACE + "ЗначенияСвойств") \
                .findall(self.NAMESPACE + "ЗначенияСвойства")
        except Exception as e:
            print('Ошибка: ', str(e))
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

            if attribute_name == 'объем':
                attribute_name = 'Объем'

            print(attribute_name, attribute_value)

            if attribute_name and attribute_value and attribute_name not in ['Направление', 'Кратность',
                                                                             'Производитель', 'Распродажа',
                                                                             'ВыгружатьЦену', 'Аналоги',
                                                                             'место хранения']:
                print("----", attribute_name, attribute_value)
                group, created = catalog_models.AttributesGroup \
                    .objects.update_or_create(title=attribute_name.replace('@', ' '))
                print(group, created)
                value, created = catalog_models.AttributeValue \
                    .objects.update_or_create(title=attribute_value)
                print(value, created)
                catalog_models.Attribute.objects.update_or_create(
                    product=product, value=value, group=group)

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
            # END 200508: VERY NEW DEACTIVATION LOGIC

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
                    print('--NEW FULL TITLE--', full_name)
        except:
            pass

        # Создание и обновление категории
        fields = ({
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
        })
        try:
            product = catalog_models.Product.objects.get(unloading_id=id_1c)
        except:
            pass
        else:
            self.set_attributes(product_xml, product)
        # if image_path_list:
        #     self.set_thumbnail(product, image_path_list[0].text.strip(" \n\t"))

        # if len(image_path_list) >= 1:
        #     for image in image_path_list[1:]:
        #         self.set_gallery_image(product, image.text.strip(" \n\t"))

    def set_gallery_image(self, product, image):
        product.product_gallery.all().delete()
        # name = image[image.rfind('/') + 1:]
        url = image
        image_media_path = os.path.join(settings.MEDIA_ROOT, 'products', url)
        image = self.create_image(image_media_path, url)
        catalog_models.ProductGallery.objects.create(
            product=product, photo=image)
        return image

    def set_thumbnail(self, instance, image_path):
        if image_path:
            image_media_path = os.path.join(
                settings.MEDIA_ROOT, 'products', image_path)
            # image_1c_path = os.path.join(self.FILE_PATH, image_path)
            thumbnail = self.create_image(image_media_path, image_path)
            instance.thumbnail = thumbnail
            instance.save()

    def create_image(self, path, name):
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
            return image
