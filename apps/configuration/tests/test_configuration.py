from django.test import TestCase
from apps.configuration.models import City

class CityTestCase(TestCase):

    def setUp(self):
        # Создаем объект City для тестирования
        self.city = City.objects.create(
            title="Test City",
            address="Test Address",
            phones="123-456-789;987-654-321",
            email="test@example.com",
            time_work="9:00 AM - 5:00 PM",
            coord_x=12.345,
            coord_y=67.890,
            work_time_start="09:00:00",
            work_time_end="17:00:00"
        )

    def test_city_creation(self):
        # Проверяем создание объекта City
        self.assertIsNotNone(self.city.id)

    def test_city_str_method(self):
        # Проверяем метод __str__
        self.assertEqual(str(self.city), "Test City")

    def test_city_phones(self):
        # Проверяем получение списка номеров телефонов
        phones = self.city.get_phones()
        self.assertEqual(len(phones), 2)
        self.assertEqual(phones[0].phone_number, "123-456-789")
        self.assertEqual(phones[1].phone_number, "987-654-321")

    def test_city_emails(self):
        # Проверяем получение списка email-ов
        emails = self.city.get_emails()
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].email, "test@example.com")

    def test_city_vacancies(self):
        # Добавьте тесты для получения списка вакансий (если у вас есть соответствующая модель Vacancy)
        pass


from django.test import TestCase
from apps.configuration.models import City, ContactEmail

class ContactEmailTestCase(TestCase):

    def setUp(self):
        # Создаем объект City для связи
        self.city = City.objects.create(
            title="Test City",
            address="Test Address",
            phones="123-456-789;987-654-321",
            email="test@example.com",
            time_work="9:00 AM - 5:00 PM",
            coord_x=12.345,
            coord_y=67.890,
            work_time_start="09:00:00",
            work_time_end="17:00:00"
        )

        # Создаем объект ContactEmail для тестирования
        self.contact_email = ContactEmail.objects.create(
            city=self.city,
            title="Test Contact Email",
            email="contact@example.com",
            show_city=True
        )

    def test_contact_email_creation(self):
        # Проверяем создание объекта ContactEmail
        self.assertIsNotNone(self.contact_email.id)

    def test_contact_email_str_method(self):
        # Проверяем метод __str__
        expected_str = "Test Contact Email (Test City)"
        self.assertEqual(str(self.contact_email), expected_str)

    def test_contact_email_city_relationship(self):
        # Проверяем связь с городом
        self.assertEqual(self.contact_email.city, self.city)

    def test_contact_email_show_city(self):
        # Проверяем флаг show_city
        self.assertTrue(self.contact_email.show_city)

    def test_contact_email_email(self):
        # Проверяем поле email
        self.assertEqual(self.contact_email.email, "contact@example.com")


from django.test import TestCase
from apps.configuration.models import SortingMixin

class SortingMixinTestCase(TestCase):

    def test_sorting_mixin_field(self):
        # Проверяем, что поле sort присутствует в модели
        self.assertTrue(hasattr(self.your_model, 'sort'))

    def test_sorting_mixin_default_value(self):
        # Проверяем, что значение по умолчанию для sort равно 1
        self.assertEqual(self.your_model.sort, 1)

    def test_sorting_mixin_custom_value(self):
        # Проверяем, что значение sort было установлено корректно
        self.assertEqual(self.your_model.sort, 42)

    def test_sorting_mixin_abstract(self):
        # Проверяем, что SortingMixin является абстрактным классом
        self.assertTrue(SortingMixin._meta.abstract)


from django.test import TestCase
from apps.configuration.models import SortingMixin, PhoneNumber, City

class PhoneNumberTestCase(TestCase):

    def setUp(self):
        # Создаем объект города, связанный с моделью PhoneNumber
        self.city = City.objects.create(
            title="Test City",
            address="Test Address"
        )
        # Создаем объект модели PhoneNumber с использованием SortingMixin
        self.phone_number = PhoneNumber.objects.create(
            city=self.city,
            title="Test Phone",
            phone="123-456-7890",
            sort=42  # Присваиваем значение сортировки
        )

    def test_sorting_mixin_field(self):
        # Проверяем, что поле sort присутствует в модели PhoneNumber
        self.assertTrue(hasattr(self.phone_number, 'sort'))

    def test_sorting_mixin_default_value(self):
        # Проверяем, что значение по умолчанию для sort равно 1
        self.assertEqual(self.phone_number.sort, 1)

    def test_sorting_mixin_custom_value(self):
        # Проверяем, что значение sort было установлено корректно
        self.assertEqual(self.phone_number.sort, 42)

    def test_phone_number_city(self):
        # Проверяем, что поле city в модели PhoneNumber имеет ожидаемое значение
        self.assertEqual(self.phone_number.city, self.city)

    def test_phone_number_title(self):
        # Проверяем, что поле title в модели PhoneNumber имеет ожидаемое значение
        self.assertEqual(self.phone_number.title, "Test Phone")

    def test_phone_number_phone(self):
        # Проверяем, что поле phone в модели PhoneNumber имеет ожидаемое значение
        self.assertEqual(self.phone_number.phone, "123-456-7890")

    def test_phone_number_str_method(self):
        # Проверяем, что метод __str__ возвращает ожидаемую строку
        expected_str = "Test Phone (Test City)"
        self.assertEqual(str(self.phone_number), expected_str)


from django.test import TestCase
from apps.configuration.models import Settings, TypeShipping


class SettingsTestCase(TestCase):

    def test_color_scheme_conversion(self):
        # Создаем объект настроек
        settings = Settings.objects.create(
            language='en',
            color_scheme='#006EFF'
        )

        # Проверяем, что метод _convert_base корректно конвертирует HEX в DEC
        self.assertEqual(settings._convert_base('006EFF', to_base=10, from_base=16), '27631')

        # Проверяем, что метод _darken корректно затемняет цвет
        self.assertEqual(settings._darken('#006EFF'), '#005BDD')

    def test_get_phones(self):
        # Создаем объект настроек с несколькими номерами телефонов
        settings = Settings.objects.create(
            language='en',
            phones='123-456-7890;987-654-3210'
        )

        # Проверяем, что метод get_phones разделяет номера корректно
        self.assertEqual(settings.get_phones(), ['123-456-7890', '987-654-3210'])

    # Добавьте другие тесты для методов и полей модели Settings


class TypeShippingTestCase(TestCase):

    def test_set_slug_field(self):
        # Создаем объект модели TypeShipping
        type_shipping = TypeShipping.objects.create(
            title='Test Type Shipping'
        )

        # Проверяем, что поле code было автоматически заполнено
        self.assertEqual(type_shipping.code, 'test-type-shipping')


from django.test import TestCase
from apps.configuration.models import Slider, Settings
from filer.models import Image

class SliderTestCase(TestCase):

    def setUp(self):
        # Создаем объект настроек сайта для использования в связи ForeignKey
        self.settings = Settings.objects.create(
            language='en',
            color_scheme='#006EFF'
        )

        # Создаем объект изображения
        self.image = Image.objects.create(
            original_filename='slider_image.jpg'
        )

    def test_slider_creation(self):
        # Создаем объект слайдера
        slider = Slider.objects.create(
            settings=self.settings,
            image=self.image,
            title='Slider Title',
            subtitle='Slider Subtitle',
            link='http://example.com',
            sort=100
        )

        # Проверяем, что объект слайдера был создан корректно
        self.assertEqual(slider.title, 'Slider Title')
        self.assertEqual(slider.subtitle, 'Slider Subtitle')
        self.assertEqual(slider.link, 'http://example.com')
        self.assertEqual(slider.sort, 100)

    def test_slider_string_representation(self):
        # Создаем объект слайдера
        slider = Slider.objects.create(
            settings=self.settings,
            image=self.image,
            title='Slider Title',
            subtitle='Slider Subtitle',
            link='http://example.com',
            sort=100
        )

        # Проверяем, что строковое представление объекта слайдера корректно
        expected_representation = 'Элемент слайдера №{}'.format(slider.id)
        self.assertEqual(str(slider), expected_representation)
