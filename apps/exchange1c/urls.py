import base64
import logging
import os
import uuid
from datetime import datetime, timedelta

from django.core import management
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from system.settings import BASE_DIR, MEDIA_ROOT

from apps.catalog.models import *

from .http_auth import http_auth

# @http_auth


@csrf_exempt
def init_1c(request):
    get_params = request.GET
    response = HttpResponse()
    session_id = request.session.session_key
    if get_params.get('mode') == 'checkauth':
        if get_params.get('type') == 'catalog':
            token = get_token(request)
            response.write(
                "success\ncsrftoken\n{}\nsessid=6dff9e4879b775e811d5e18dcc615412\ntimestamp=1527775445".format(token))
            return response

    if get_params.get('mode') == 'init':
        response.write("zip=no\nfile_limit=1073741824")
        return response

    if get_params.get('mode') == 'file':
        file_path = BASE_DIR + '/../1c/' + get_params.get('filename')

        if get_params.get('filename').endswith('.xml'):
            print("later")
            file_path = BASE_DIR + '/../1c/' + get_params.get('filename')
            if len(get_params.get('filename').split('/')) > 1:
                # получаем директории без файла
                os.makedirs(
                    BASE_DIR + '/../1c/' + "/".join(get_params.get('filename').split('/')[:-1]), exist_ok=True)
        else:
            file_path = MEDIA_ROOT + '/products/' + \
                get_params.get('filename')
            if len(get_params.get('filename').split('/')) > 1:
                os.makedirs(MEDIA_ROOT + '/products/' + "/".join(get_params.get('filename').split('/')[:-1]),
                            exist_ok=True)
        with open(file_path, 'wb') as outfile:
            outfile.write(request.body)

        response.write("success")

        return response

    if get_params.get('mode') == 'import':
        STATUS_FILENAME = "1cbitrix"
        file_name = get_params.get("filename")
        print(file_name)
        if get_params.get('filename').endswith('.xml'):
            if STATUS_FILENAME in file_name:
                management.call_command("parse_status", filename=file_name)
            elif get_params.get('type') == 'dogovor':
                management.call_command("parse_contract", filename=file_name)
            else:
                management.call_command(
                    'parse', in_action=1, filename=get_params.get('filename'))

        response.write("success")

        return response
    # orders = Order.objects.exclude(status_imported='upload') # BAD! BAD MISHA!
    orders = Order.objects.filter(status_imported='processing')
    print(orders)
    if get_params.get('mode') == 'query':
        if get_params.get('type') == 'sale':
            if get_params.get('debug'):
                orders = Order.objects.filter(id__in=[222])
            return generate_sales(request, orders)

    if get_params.get('mode') == 'success':
        if get_params.get('type') == 'sale':
            last_date = Settings.load()
            last_date.last_export_date = datetime.now()
            last_date.save()
            orders.update(status_imported='upload')
            response.write("success")
            return response
    response.write(
        "success\nPHPSESSID\nft9b1rcl11r3c16kf97b842113\nsessid=6dff9e4879b775e811d5e18dcc615412\ntimestamp=1527775445")
    return response


# \?type=catalog&mode=init/
# \?type=catalog&mode=file&filename=(?P<slug>[\w-]+)/
# \?type=catalog&mode=import&filename=(?P<slug>[\w-]+)/
# \?type=sale&mode=checkauth
# \?type=catalog&mode=file&filename=(?P<slug>[\w-]+)/
# \?type=catalog&mode=import&filename=(?P<slug>[\w-]+)/

from datetime import datetime
#
from decimal import Decimal
from xml.dom import minidom
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree, SubElement

import requests
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db.models import Sum
from django.shortcuts import render
from filer.models import Image

from apps.exchange1c.api import OrderXML
from apps.shop.models import Order

from .models import Settings


def prettify(elem):
    rough_string = ET.tostring(elem, u'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='   ')


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    file_name = f'{MEDIA_ROOT}/logs/{get_logger_filename()}'
    file_handler = logging.FileHandler(str(file_name))
    logger.addHandler(file_handler)
    file_handler.setFormatter(logging.Formatter(
        fmt='[%(asctime)s: %(levelname)s] %(message)s')
    )
    logger.setLevel(logging.DEBUG)
    return logger


def get_logger_filename() -> str:
    return f'orders_exchange_{datetime.now()}.log'


def generate_sales(request, orders=None):
    logger = setup_logger()
    if request.GET.get('debug'):
        orders = Order.objects.filter(
            id__in=request.GET.get('debug', '').split(','))
    orders = orders or Order.objects.filter(
        status_imported__in=['not_upload', 'processing']).all()
    orders = orders.annotate(items_count=Sum('order_items__count')) \
        .filter(items_count__gt=0) \
        .all()
    logger.info(
        '[ORDERS EXCHANGE] Идентификаторы заказов к обмену: %s', list(orders.values_list('id')))
    orders.update(status_imported='processing')
    root = OrderXML().create(orders)
    root = '<?xml version="1.0" encoding="UTF-8"?>\n' + prettify(root)
    root = root.replace('<?xml version="1.0" ?>\n', "")
    response = HttpResponse(content_type='text/xml')
    response.write(root.encode('UTF-8'))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response


def generate_yml():
    # <?xml version="1.0" encoding="UTF-8"?>
    # <yml_catalog date="2017-02-05 17:22">
    root = Element('yml_catalog')
    now = datetime.now()
    root.set('date', now.date().isoformat())

    shop_y = SubElement(root, 'shop')
    # <name>BestSeller</name>
    # <company>Tne Best inc.</company>
    # <url>http://best.seller.ru</url>
    # <currencies>
    #   <currency id="RUR" rate="1"/>
    #   <currency id="USD" rate="60"/>
    # </currencies>
    categories_y = SubElement(shop_y, 'categories')
    categories = Category.objects.filter(active=True)
    for category in categories:
        category_y = SubElement(categories_y, 'category')
        category_y.set('id', category.id)
        category_y.text = category.title
        if category.parent:
            category_y.set('parentId', category.parent.id)

    # <delivery-options>
    #   <option cost="300" days="0" order-before="12"/>
    # </delivery-options>

    offers_y = SubElement(shop_y, 'offers')
    products = Product.objects.filter(active=True)
    for product in products:
        offer_y = SubElement(offers_y, 'offer')
        SubElement(offer_y, 'url').text = product.get_absolute_url()
        SubElement(offer_y, 'price').text = product.price
        SubElement(offer_y, 'currencyId').text = "RUR"
        SubElement(offer_y, 'categoryId').text = product.category.id
        if product.old_price:
            SubElement(offer_y, 'oldprice').text = product.old_price
        if product.thumbnail:
            SubElement(offer_y, 'oldprice').text = product.thumbnail.url
        SubElement(offer_y, 'name').text = product.title.replace("&", "")
        SubElement(
            offer_y, 'description').text = "<![CDATA[" + product.description.replace("&", "") + "]]>"
    root = '<?xml version="1.0" encoding="windows-1251"?>\n' + prettify(root)
    root = root.replace('<?xml version="1.0" ?>\n', "")
    response = HttpResponse(content_type='text/xml')
    response.write(root.encode('cp1251'))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return root


# <store>false</store>
# <pickup>true</pickup>
# <delivery>true</delivery>
# <delivery-options>
#   <option cost="300" days="0" order-before="12"/>
# </delivery-options>
# <name>Вафельница First FA-5300</name>
# <vendor>First</vendor>
# <vendorCode>A1234567B</vendorCode>
# <description>
# <![CDATA[
#   <p>Отличный подарок для любителей венских вафель.</p>
# ]]>
# </description>
# <sales_notes>Необходима предоплата.</sales_notes>
# <manufacturer_warranty>true</manufacturer_warranty>
# <country_of_origin>Россия</country_of_origin>
# <barcode>0156789012</barcode>


urlpatterns = [
    path('1c_exchange.py', init_1c, name='init_1c'),
    path('1c_exchange.xml', generate_sales, name='init_1c1'),
    path('catalog.yml', generate_yml, name='generate_yml'),
]
