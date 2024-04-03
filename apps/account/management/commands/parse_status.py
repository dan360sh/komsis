from typing import Iterable
from django.core.management.base import BaseCommand
from apps.account.models import Account, AccountStatus
from apps.shop.models import Order, OrderState
from system import settings
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
import os


class Command(BaseCommand):
    DEFAULT_FILE_NAME = "FILE_DOESNOT_EXIST"
    FILE_PATH = settings.BASE_DIR + '/../1c/'

    ORDER_OPERATION_TITLE = "Заказ товара"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--filename", default=self.DEFAULT_FILE_NAME)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        filename = options.get("filename")
        if not self.is_file_exists(filename):
            raise IOError("Файла импорта не существует")

        file_path = os.path.join(self.FILE_PATH + filename)
        document_root = ET.parse(file_path).getroot()
        if not self.is_status_import_file(document_root):
            raise AttributeError("Файл не является файлом импорта статусов")
        print("\n============================\n")
        print("Выгрузка статусов")
        for document in document_root.findall("Документ"):
            self.parse_document(document)

    def parse_document(self, document: Element):
        persons_block = document.find("Контрагенты")
        for person in persons_block.findall("Контрагент"):
            self.parse_person(person)
        # Обновление полей заказа
        order_id = document.find("Номер").text
        order = self.get_order(order_id)
        if order is None:
            print(f"Заказ не найден {order_id}")
            return
        # Перед добавлением выполненных статусов
        # удалим их все
        print(f"Загрузка заказа #{order.id}")
        order.completed_states.clear()
        order_states_block = document.find("СтатусыЗаказа")
        order_completed_states = self.get_order_states(order_states_block)
        for state in order_completed_states:
            order.add_completed_state(state)
        # После добавления выполненных статусов заказа
        # берем их, соритруем по возрастанию их порядка,
        # забираем последний статус и делаем его текущим
        last_state = order.completed_states.all().order_by("position").last()
        if last_state is None:
            print(f"Заказ без состояний #{order.id}")
            return
        order.set_current_state(last_state)
        # Проверяем обновленные состояния на наличие подтвержденного
        if order.has_confirmed_state:
            order.mark_as_confirmed()

    def parse_person(self, person: Element):
        """Разбор переданного блока контрагента.

        Если пользователь был найден по данным из файла выгрузки,
        его поля `(id_1c, status)` будут обновлены,
        иначе он будет просто пропущен

        Args:
            person (Element): Блок из файла выгрузки
        """
        full_name_block = person.find("Наименование")
        if full_name_block is None:
            return print("У блока пользователя не найдено имя!")
        full_name = full_name_block.text
        account = Account.find_by_name(full_name)
        person_uuid = person.find("Ид").text
        account = self.get_account(full_name, person_uuid)
        if account is None:
            print(f"Не удалось найти аккаунт {full_name}, id: {person_uuid}")
            return
        print(f"UUID: {person_uuid}")
        account.update_uuid(person_uuid)
        person_status = self.get_person_status(person)
        if person_status is None:
            return
        print(f"Статус: {person_status.title}")
        account.update_status(person_status)

    def get_account(self, name, uuid):
        """Получить аккаунт по ФИО и ИД из 1с.

        Сначала ищем по полю ИД, если совпадений нет,
        то по ФИО

        Args:
            name (str): ФИО пользователя
            uuid (srt): ИД из 1с

        Returns:
            Account: Если было найдено совпадение, то инстанс Account,
            иначе NoneType
        """
        # Сначала ищем по ИД из 1с, но,
        # так как ИД из 1с появились в бд сайта не сразу, то
        # если пользователь не был найден по ИД
        # пробуем найти его по ФИО
        result = Account.find_by_uuid(uuid)
        if result is None:
            result = Account.find_by_name(name)
        return result

    def get_person_status(self, person: Element) -> AccountStatus:
        """Получаем текущий статус аккаунта из переданного
        блока xml.

        Args:
            person (Element): Блок из файла выгрузки

        Returns:
            AccountStatus: Найденный статус аккаунта
        """
        status_block = person.find("СтатусКонтрагента")
        if status_block is None:
            return
        id_block = status_block.find("Код")
        if id_block is None:
            return
        return AccountStatus.objects.get(code=id_block.text)

    def get_order(self, id_: str) -> Order:
        """Получить заказ исходя из переданного ИД.

        Returns:
            Order: заказ
        """
        try:
            return Order.objects.get(id=id_)
        except Order.DoesNotExist:
            return None

    def get_order_states(self, states_block: Element) -> Iterable[OrderState]:
        """Получить все состояния заказа, которые содержит документ.

        Состояния, которые содержатся в документе считаются
        выполненными

        Args:
            states_block (Element): Блок из файла выгрузки

        Returns:
            Iterable[OrderState]: Перечисление всех состояний из файла выгрузки
        """
        result = list()
        for state_elem in states_block.findall("Статус"):
            state_id = state_elem.find("Код").text
            state = OrderState.objects.get(code=state_id)
            result.append(state)
        return result

    def is_file_exists(self, filename) -> bool:
        """Проверка директории файлов выгрузки на
        существования в ней переданного имени файла.

        Args:
            filename (str): Имя файла, с его расширением

        Returns:
            bool: Результат проверки
        """
        return filename != self.DEFAULT_FILE_NAME and\
            os.path.isfile(self.FILE_PATH + filename)

    def is_status_import_file(self, root: Element) -> bool:
        """Проверка документа на то, что он соответсвует шаблону
        файла выгрузки статусов заказов и пользователей.

        Args:
            root (Element): `Корневой` элемент документа

        Returns:
            bool: Результат проверки
        """
        document = root.findall("Документ")[0]
        operation_title = document.find("ХозОперация")
        return operation_title.text == self.ORDER_OPERATION_TITLE
