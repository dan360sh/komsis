from django.core.management.base import BaseCommand
from apps.account.models.Account import Account
from apps.catalog.models import PriceType
from system import settings
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
import os


class Command(BaseCommand):
    DEFAULT_FILE_NAME = "NONAME.xml"
    FILE_PATH = settings.BASE_DIR + '/../1c/'
    
    def add_arguments(self, parser) -> None:
        parser.add_argument("--filename", default=self.DEFAULT_FILE_NAME)
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        filename = options.get("filename")
        file_path = os.path.join(self.FILE_PATH + filename)
        document_root = ET.parse(file_path).getroot()
        for document in document_root.findall("Договор"):
            self.parse_document(document)

    def parse_document(self, document: Element):
        document_rows = document.find("ЗначенияРеквизитов")
        contract_title: str = ""
        account_inn: str = ""
        contract_type: str = ""
        price_type_title: str = ""
        contract_balance: float = float(0)
        for row in document_rows.findall("ЗначениеРеквизита"):
            title = row.find("Наименование")
            value = row.find("Значение")
            if title.text == "Наименование":
                contract_title = value.text
            elif title.text == "КонтрагентИНН":
                account_inn = value.text
            elif title.text == "ТипДоговора":
                contract_type = value.text
            elif title.text == "ТипЦен":
                price_type_title = value.text
            elif title.text == "Баланс":
                contract_balance = float(value.text)
        
        SEPARATOR = "=================================================="
        print(SEPARATOR)
        
        message_to_print = f"""
        Наименование договора: {contract_title}
        ИНН: {account_inn}
        Тип договора: {contract_type}
        Тип цены: {price_type_title}
        Баланс договора: {contract_balance}
        """
        print(message_to_print)
        if account_inn is None or account_inn == "":
            print("Пустое значение ИНН")
            return
        account: Account = Account.get_account(inn=account_inn)
        if account is None:
            print("Аккаунт не найден")
            return
        price_type = PriceType.get_by_title(price_type_title)
        if price_type is None:
            print(f"Тип цены {price_type_title} не найден")
            return
        account.contract_name = contract_title
        account.contract_type = contract_type
        account.contract_balance = contract_balance
        account.price_type = price_type
        account.save()
