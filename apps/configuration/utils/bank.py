import json
import logging
from datetime import datetime as dt

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.urls import reverse
from django.utils import timezone
from filer.models import File

from apps.configuration.models import Settings
from apps.shop.models import Order
from apps.shop.models.order import OrderLog

from .send_emails import send_order_emails

FILE_HANDLER_NAME = "FILE_HANDLER_NAME"


class BankResponseKeyError(Exception):
    pass


class BankPayment:
    def __init__(self, order, request=None):
        super(BankPayment, self).__init__()
        settings = Settings.objects.first()
        if not settings:
            settings = Settings(language="fallback")
        if request is None:
            schema = "https"
            host = "komsis.su"
        else:
            schema = request.META.get("REQUEST_SCHEME", None) or "https"
            host = request.META.get("HTTP_HOST", None) or "komsis.su"
        return_url = "{0}://{1}{2}".format(schema, host, reverse("validate-payment"))

        self.area = settings.mode_payment
        self.shop_id = settings.shop_id
        self.api_key = settings.api_key
        self.order: Order = order
        self.return_url = return_url
        self.logger = self.setup_logger()
        self.request = request

    def is_valid(self):
        # all([self.area, self.shop_id, self.api_key, self.order, self.return_url])
        if (
            self.area
            and self.shop_id
            and self.api_key
            and self.order
            and self.return_url
        ):
            return True
        return False

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)
        file_name = f"{settings.MEDIA_ROOT}/logs/{self._get_logger_filename()}"
        file_handler = logging.FileHandler(str(file_name))
        file_handler.set_name(FILE_HANDLER_NAME)
        logger.addHandler(file_handler)
        file_handler.setFormatter(
            logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
        )
        return logger

    def _get_logger_filename(self) -> str:
        return f"order{self.order.id}.log"

    def register_payment(self):
        """Регистрируем заказ в системе сбербанка

        amount - Сумма заказа задается в копейках

        returnUrl - Ссылка для перенаправления после оплаты
        """
        DO = "register.do"

        data = {
            "userName": self.shop_id,
            "password": self.api_key,
            "orderNumber": self.order.id,
            # data = {'userName': self.shop_id, 'password': self.api_key, 'orderNumber': 'FNRTEST'+\
            # str(dt.now()).translate(str.maketrans('','','-:. ')),
            "amount": int(self.order.total * 100),
            "returnUrl": self.return_url,
        }
        self.logger.info("Регистрация транзакции в системе")

        orderBundle = {"cartItems": {"items": list()}}
        # n=iter(range(0,100))
        for item in self.order.order_items.all():
            orderBundle["cartItems"]["items"].append(
                {
                    "positionId": item.product.id,
                    "name": item.product.title,
                    "quantity": {
                        "value": item.count,
                        "measure": item.product.unit,
                    },
                    "itemCode": str(item.product.id),
                    "tax": {"taxType": 6, "taxSum": 20},  # VAT 20%
                    # yep, it's a one unit price field
                    "itemPrice": int(item.total * 100),
                    "itemAttributes": {
                        "attributes": [
                            {
                                "name": "paymentMethod",
                                "value": "1",
                            },
                            {
                                "name": "paymentObject",
                                "value": "1",
                            },
                        ]
                    },
                }
            )

        if orderBundle:
            data["orderBundle"] = json.dumps(orderBundle)
        # print('REQ DATA: ' + str(json.dumps(data, indent=4)))
        resp = requests.post(self.area + "rest/" + DO, data=data, verify=False).text
        response_data = json.loads(resp)
        self.logger.info(f"Ответ от банковской системы: {response_data}")
        # print('BANK RESPONSE: ' + str(response_data))
        bank_id = response_data.get("orderId", None)
        if bank_id is None:
            self.logger.error(
                "Ответ от банковской системы содержал ошибки, отмена операции..."
            )
            self.save_log_file()
            raise BankResponseKeyError("There is no orderId in response")
        self.order.bank_id = bank_id
        self.order.save()

        redirect = response_data["formUrl"]

        if not bank_id or not redirect:
            return ""
        self.save_log_file()
        return redirect

    def save_log_file(self):
        file_name = f"{settings.MEDIA_ROOT}/logs/{self._get_logger_filename()}"
        user = User.objects.filter(is_superuser=True).first()
        with open(file_name, "rb") as file_:
            file_obj = DjangoFile(file_, name=self._get_logger_filename())
            file_model = File.objects.create(
                owner=user,
                original_filename=str(self._get_logger_filename()),
                file=file_obj,
            )
            _ = OrderLog.objects.create(
                order=self.order, log_file=file_model, date=timezone.now()
            )
        return

    def set_status_order(self):
        """Проверяем оплату заказа и ставим статус"""

        DO = "getOrderStatus.do"
        data = {
            "userName": self.shop_id,
            "password": self.api_key,
            "orderId": self.order.bank_id,
        }
        response_data = json.loads(
            requests.post(self.area + "rest/" + DO, data=data, verify=False).text
        )
        if (
            response_data.get("OrderStatus", False)
            and response_data["OrderStatus"] == 2
        ):
            self.order.payment = True
            self.order.status_imported = "not_upload"
            send_order_emails(self.order, self.request)
            self.order.remove_from_stash()
            self.order.save()
            return True
        return False
