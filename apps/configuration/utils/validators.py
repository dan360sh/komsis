from apps.account.models import Account
import re


class Validator:
    def __init__(self, data, user):
        self._data = data
        self._user = user
        self.fields = {}
        self.validate_form()
        has_password = self._data.get('password', None)
        if has_password:
            self.validate_password_form()

    def validate_form(self):
        self.validate_email()
        self.validate_phone()
        jurical = self._data.get('jurical', False)
        if jurical:
            self.validate_company_name()
            self.validate_inn()

    def validate_password_form(self):
        self.validate_password_repeat()

    def validate_email(self):
        email = self._data.get('email', '')
        if email == '':
            self.add_error('email', 'Заполните почтовый адрес')
            return

        account_list = Account.objects.filter(email=email).exclude(user=self._user)
        if account_list.exists():
            self.add_error('email', 'Почтовый адрес уже зарегестрирован')
            return

        return True

    def validate_phone(self):
        phone = self._data.get('phone', '')
        if phone == '':
            self.add_error('phone', 'Введите номер телефона')
            return

        account_list = Account.objects.filter(phone=phone).exclude(user=self._user)
        if account_list.exists():
            self.add_error('phone', 'Телефон уже зарегестрирован')
            return

        LENGTH = 11
        FIRST_NUMS = (7, 8)
        clear_phone = re.sub('[^\d]', '', phone)
        if len(clear_phone) != LENGTH:
            self.add_error('phone', 'Неверная длина номера телефона')
            return

        elif int(clear_phone[0]) not in FIRST_NUMS:
            self.add_error('phone', 'Телефон не принадлежит российскому провайдеру')
            return

        return True

    def validate_password_repeat(self):
        password = self._data.get('password', '')
        password_repeat = self._data.get('password_repeat', '')

        if password == '':
            self.add_error('password', 'Заполните пароль')

        if password_repeat == '':
            self.add_error('password_repeat', 'Повторите пароль')

        if password_repeat != password:
            self.add_error('password', 'Пароли не совпадают')
            self.add_error('password_repeat', 'Пароли не совпадают')
            return

        return True

    def validate_company_name(self):
        title = self._data.get('company_title', '')
        if title == '':
            self.add_error('company_title', 'Заполните наименование организации')
            return

        return True

    def validate_inn(self):
        inn = self._data.get('company_inn', '')
        if len(inn) != 10 and len(inn) != 12:
            self.add_error('company_inn', 'Неверная длина ИНН')
            return

        account_list = Account.objects.filter(company_inn=inn).exclude(user=self._user)
        if account_list.exists():
            self.add_error('company_inn', 'ИНН уже зарегестрирован')
            return

        return True

    def add_error(self, field_name, msg):
        self.fields[field_name] = msg

    @property
    def has_errors(self):
        if self.fields:
            return True

        return False
