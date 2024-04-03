from datetime import datetime
from django.conf import settings
from lxml import etree as xml
import uuid
from django.utils import timezone
from django.utils.timezone import get_current_timezone


class OrderXML:

    def __init__(self, order=None):
        self.order = order
        self.ed_izm = {
            'м': {
                'Код': '006',
                'Наименованиеполное': 'Метр',
            },
            'шт': {
                'Код': 796,
                'МеждународноеСокращение': 'PCE',
                'НаименованиеПолное': 'Штука'
            },
            'кг': {
                'Код': 166,
                'НаименованиеПолное': "Килограмм",
                'МеждународноеСокращение': "KGM",
            },
            'компл.': {
                'Код': 839,
                'НаименованиеПолное': "Комплект",
            },
        }

    def create(self, orders, printed=False):
        """Сборка документа"""
        root = xml.Element(u'КоммерческаяИнформация')
        attrs = {
            'ВерсияСхемы': 2.09,
            'ДатаФормирования': datetime.now().date().isoformat(),
        }
        self.__add_value(root, attrs, is_subelements=False)
        for order in orders:
            if order.total and order.order_items \
                    .filter(product__isnull=False, count__gt=0) \
                    .exists():
                self.order = order
                document = self.add_document(root)
                self.add_contractors(document)
                date = timezone.make_naive(self.order.date)
                self.__add_value(document, {'Дата': date.date()})
                self.__add_value(document, {'Время': date.time().strftime('%H:%M:%S')})
                self.__add_value(document, {'Комментарий': self.order.comment})
                self.add_products(document)
                self.add_requisites(document)
        if printed:
            self.print(root)
        return root

    def add_document(self, block):
        """Документ"""
        document = xml.SubElement(block, 'Документ')

        shipping_address = self.order.shop_address
        if self.order.shipping != 'self':
            shipping_address = self.order.get_shipping_address()

        attrs = {
            'Ид': self.order.id,
            'Номер': self.order.id,
            # 'Дата': self.order.date.date(), # no timezone applied
            'ХозОперация': 'Заказ товара',
            'Роль': 'Продавец',
            'Валюта': 'руб',
            'Курс': 1,
            'Сумма': self.order.total,
            'СуммаБезБонусов': self.order.total_without_points,
            'БонусовПотрачено': self.order.points_spent,
            'БонусовПолучено': self.order.points_collected,
            'СпособПолучения': self.order.get_shipping_display(),
            'АдресПолучения': shipping_address
        }
        self.__add_value(document, attrs)
        return document

    def add_contractors(self, block):
        """Контрагенты"""
        contractors = xml.SubElement(block, 'Контрагенты')
        contractor = xml.SubElement(contractors, 'Контрагент')
        attrs = {
            'Ид': self.get_account_id(),
            'Наименование': self.order.name,
            'Роль': 'Покупатель',
            'ПолноеНаименование': self.order.person_fullname,
        }
        attrs['Фамилия'] = self.order.surname
        attrs['Имя'] = self.order.name
        attrs['Отчество'] = self.order.middle_name
        if self.order.account:
            if self.order.account.bonus_card_id:
                attrs["НомерБонуснойКарты"] = self.order.account.bonus_card_id
        self.__add_value(contractor, attrs)
        self.add_address(contractor)
        self.add_contacts(contractor)
        self.add_representatives(contractor)
        return contractors

    def add_address(self, block):
        """Адрес регистрации"""
        address = xml.SubElement(block, 'АдресРегистрации')
        # Список полей адреса
        address_fields = {
            'Область': self.order.region,
            'Район': self.order.district,
            'Нас. пункт': self.order.city,
            'Улица': self.order.street,
            'Дом': self.order.house,
            'Корпус': self.order.housing,
            'Квартира': self.order.apartment,
        }
        # Представление полного адреса
        full_address = ','.join([
            key + ' ' + str(value)
            for key, value in address_fields.items()
            if value
        ])

        attrs = {'Представление': full_address}
        self.__add_value(address, attrs)
        # Добавление каждого поля адреса отдельно
        self.__add_subvalues(
            address, 'АдресноеПоле', 'Тип', 'Значение', address_fields)
        return address

    def get_account_id(self):
        return self.order.account.id if self.order.account else str(uuid.uuid4())

    def __add_value(self, block, values: dict, is_subelements: bool = True):
        """Добавление значение"""
        attr = None
        if is_subelements:
            for title, value in values.items():
                attr = xml.SubElement(block, title)
                attr.text = str(value)
        else:
            for title, value in values.items():
                block.set(title, str(value))
        return attr

    def __add_subvalues(self, block, iter_block: str,
                        key: str, value: str, attrs: dict):
        """
        :block: Xml Block к которому привязываются значения
        :iter_block: Название итерируемого блока
        :key: Первое значение
        :value: Второе значение
        :attrs: Словарь значений
        """
        for xml_field, field_value, in attrs.items():
            attr_block = xml.SubElement(block, iter_block)
            attrs = {
                key: xml_field,
                value: field_value,
            }
            self.__add_value(attr_block, attrs)

    def add_contacts(self, block):
        """Блок контакты"""
        contacts = xml.SubElement(block, 'Контакты')
        attrs = {
            'Почта': self.order.email,
            'Телефон рабочий': self.order.phone
        }
        self.__add_subvalues(contacts, 'Контакт', 'Тип', 'Значение', attrs)
        return contacts

    def add_representatives(self, block):
        """Блок представители"""
        representatives = xml.SubElement(block, 'Представители')
        representative = xml.SubElement(representatives, 'Представитель')
        self.__add_value(representative, {'Отношение': 'Контактное лицо'})
        self.__add_value(representative, {'Ид': self.get_account_id()})
        self.__add_value(representative, {'Наименование': self.order.person_fullname})
        return representatives

    def add_products(self, block):
        """Блок продукты"""
        products = xml.SubElement(block, 'Товары')
        for item in self.order.order_items.filter(count__gt=0).iterator():
            if item.product:
                product = xml.SubElement(products, 'Товар')
                option = item.option if item.option else ""
                attrs = {
                    'Ид': item.product.unloading_id,
                    'Наименование': item.product.title,
                    'Характеристика': option,
                    'БазоваяЕдиница': item.product.unit,
                }

                ed = self.__add_value(product, attrs)
                # ed izm
                if ed is not None or ed not in self.ed_izm.keys():
                    ed_izm = 'шт'
                attrs = self.ed_izm.get(ed_izm)
                self.__add_value(ed, attrs, False)

                attrs = {
                    'ЦенаЗаЕдиницу': item.total,
                    'Количество': item.count,
                    'Сумма': item.total_price(),
                }
                self.__add_value(product, attrs)
        return products

    def toCamelCase(self, name: str) -> str:
        """Превращает строку в верблюжий регистр"""
        return ''.join(map(str.title, name.split(' ')))

    def add_requisites(self, block):
        """Значения реквизитов"""
        requisites = xml.SubElement(block, 'ЗначенияРеквизитов')
        inn = self.order.company_inn
        company_title = self.order.company_title

        if not self.order.jurical:
            inn = ""
            company_title = ""

        attrs = {
            'Заказ Оплачен': self.order.payment,
            'Статус': self.order.get_status_display(),
            'Способ Оплаты': self.order.get_type_payment_display(),
            'Доставка': self.order.shipping_type_name or self.order.get_shipping_display(),
            'Название компании': company_title,
            'Инн компании': inn,
        }
        self.__add_value(requisites,
                         # {self.toCamelCase(name): attr for name, attr in attrs.items() if attr})
                         {self.toCamelCase(name): attr for name, attr in attrs.items()})
        # self.__add_subvalues(
        #     requisites, 'ЗначениеРеквизита', 'Наименование', 'Значение', attrs)
        return requisites

    def print(self, block):
        """Принт документа"""
        result = xml.tostring(block, pretty_print=True, encoding='UTF-8').decode('UTF-8')
        print(result)
        return result
