from django.test import TestCase
from apps.shop.models import Cart, CartItem

class CartModelTestCase(TestCase):

    def test_cart_creation(self):
        # Проверяем, что объект Cart был создан корректно
        self.assertEqual(self.cart.account, self.account)


class CartItemModelTestCase(TestCase):

    def test_cart_item_creation(self):
        # Проверяем, что объект CartItem был создан корректно
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)

    def test_cart_item_price(self):
        # Проверяем, что метод price() элемента корзины возвращает правильную цену
        self.assertEqual(self.cart_item.price(), 10.0)

    def test_cart_item_total(self):
        # Проверяем, что метод total() элемента корзины возвращает правильную общую стоимость
        self.assertEqual(self.cart_item.total(), 30.0)

    def test_cart_item_count_price_by_account(self):
        # Проверяем, что метод count_price_by_account() элемента корзины возвращает правильную цену для аккаунта
        self.assertEqual(
            self.cart_item.count_price_by_account(self.account), 10.0)

    def test_cart_item_count_total_by_account(self):
        # Проверяем, что метод count_total_by_account() элемента корзины возвращает правильную общую стоимость для аккаунта
        self.assertEqual(
            self.cart_item.count_total_by_account(self.account), 30.0)

from django.test import TestCase
from apps.shop.models import Compare

class CompareModelTestCase(TestCase):

    def test_compare_creation(self):
        # Создаем объект Compare и привязываем его к Account
        compare = Compare.objects.create(account=self.account)

        # Проверяем, что объект Compare был создан корректно
        self.assertEqual(compare.account, self.account)

    def test_compare_items(self):
        # Создаем объект Compare и привязываем его к Account
        compare = Compare.objects.create(account=self.account)

    def test_compare_count(self):
        # Создаем объект Compare и привязываем его к Account
        compare = Compare.objects.create(account=self.account)

        # Проверяем, что количество товаров в сравнении соответствует ожиданиям
        self.assertEqual(compare.count(), 5)


from django.test import TestCase
from apps.shop.models import Compare, CompareItem
from django.db.models.signals import post_save
from django.dispatch import receiver

class CompareItemModelTestCase(TestCase):

    def test_compare_item_creation(self):
        # Создаем объект Compare и привязываем его к Account
        compare = Compare.objects.create(account=self.account)


from django.test import TestCase
from apps.shop.models import UnauthCompare, UnauthCompareItem

class UnauthCompareTestCase(TestCase):

    def test_unauth_compare_items(self):
        # Создайте несколько элементов UnauthCompareItem для теста
        item1 = UnauthCompareItem(product="Product 1")
        item2 = UnauthCompareItem(product="Product 2")

        # Создайте объект UnauthCompare и передайте в него элементы
        unauth_compare = UnauthCompare(compare_items=[item1, item2])

        # Проверьте, что метод items() возвращает список элементов
        items = unauth_compare.items()
        self.assertEqual(len(items), 2)
        self.assertIn(item1, items)
        self.assertIn(item2, items)

        # Проверьте, что метод count() возвращает правильное количество элементов
        count = unauth_compare.count()
        self.assertEqual(count, 2)


from django.test import TestCase
from apps.shop.models import UnauthCompareItem

class UnauthCompareItemTestCase(TestCase):

    def test_unauth_compare_item_creation(self):
        # Создайте элемент UnauthCompareItem
        product_name = "Test Product"
        item = UnauthCompareItem(product=product_name)

        # Проверьте, что элемент был создан корректно
        self.assertEqual(item.product, product_name)

from django.test import TestCase
from apps.shop.models import Favorites, FavoritesItem
from django.contrib.auth.models import User

class FavoritesItemTestCase(TestCase):

    def test_favorites_item_creation(self):
        # Создаем объект FavoritesItem и связываем его с Favorites и продуктом
        favorites_item = FavoritesItem.objects.create(favorites=self.favorites, product=self.product1)

        # Проверяем, что объект FavoritesItem был создан корректно
        self.assertEqual(favorites_item.favorites, self.favorites)
        self.assertEqual(favorites_item.product, self.product1)

    def test_create_favorites_signal(self):
        # Проверяем, что при создании пользователя создается объект Favorites
        self.assertEqual(Favorites.objects.filter(account=self.account).count(), 1)

    def test_save_favorites_signal(self):
        # Меняем имя пользователя и сохраняем его
        self.user.username = 'new_username'
        self.user.save()

        # Проверяем, что объект Favorites также был сохранен
        favorites = Favorites.objects.get(account=self.account)
        self.assertEqual(favorites.account, self.account)
        self.assertEqual(favorites.account.user.username, 'new_username')

from django.test import TestCase
from apps.shop.models import UnauthFavorites, UnauthFavoritesItem

class UnauthFavoritesTestCase(TestCase):

    def setUp(self):
        # Создаем неавторизованный пользователь (или что-то, что будет представлять его)
        self.unauth_user = 'unauth_user_id'

        # Создаем объект UnauthFavorites
        self.unauth_favorites = UnauthFavorites()

        # Создаем продукты
        self.product1 = {'id': 1, 'name': 'Product 1'}
        self.product2 = {'id': 2, 'name': 'Product 2'}

    def test_unauth_favorites_item_creation(self):
        # Создаем объект UnauthFavoritesItem и добавляем его к UnauthFavorites
        unauth_favorites_item = UnauthFavoritesItem(product=self.product1)
        self.unauth_favorites.add(unauth_favorites_item)

        # Проверяем, что объект UnauthFavoritesItem был добавлен корректно
        self.assertEqual(len(self.unauth_favorites.items()), 1)
        self.assertEqual(self.unauth_favorites.items()[0].product, self.product1)

    def test_count_unauth_favorites_items(self):
        # Создаем объекты UnauthFavoritesItem и добавляем их к UnauthFavorites
        unauth_favorites_item1 = UnauthFavoritesItem(product=self.product1)
        unauth_favorites_item2 = UnauthFavoritesItem(product=self.product2)
        self.unauth_favorites.add(unauth_favorites_item1)
        self.unauth_favorites.add(unauth_favorites_item2)

        # Проверяем, что количество элементов считается правильно
        self.assertEqual(self.unauth_favorites.count(), 2)

from django.test import TestCase
from apps.shop.models import UnauthFavoritesItem

class UnauthFavoritesItemTestCase(TestCase):

    def setUp(self):
        # Создаем продукт для теста
        self.product = {'id': 1, 'name': 'Test Product'}

    def test_unauth_favorites_item_creation(self):
        # Создаем объект UnauthFavoritesItem
        unauth_favorites_item = UnauthFavoritesItem(product=self.product)

        # Проверяем, что объект UnauthFavoritesItem был создан корректно
        self.assertEqual(unauth_favorites_item.product, self.product)

from django.test import TestCase
from datetime import datetime
from apps.shop.models import Order, OrderState

class OrderModelTestCase(TestCase):

    def test_order_creation(self):
        # Тест на создание объекта Order
        order = Order.objects.create(
            account=self.account,
            surname='Smith',
            name='John',
            phone='1234567890',
            email='test@example.com',
            date=datetime.now(),
            total=100.0,
            status='processing',
            type_payment='receiving',
            shipping='self',
            shipping_price=0,
            post_code=12345,
            region='Test Region',
            district='Test District',
            city='Test City',
            street='Test Street',
            house='123',
            housing='A',
            apartment='45',
            entrance='1',
            comment='Test Comment',
            shipping_type_name='Test Shipping Type',
            status_imported='not_upload',
            shop_address='Test Shop Address',
            company_title='Test Company',
            company_inn='1234567890',
            payment_file='test.pdf',
            jurical=False,
            total_without_points=90.0,
            points_spent=10.0,
            points_collected=10.0,
            is_deleted=False,
            is_confirmed=False,
            current_state=self.state,
        )

        self.assertEqual(order.account, self.account)
        self.assertEqual(order.surname, 'Smith')
        self.assertEqual(order.name, 'John')
        self.assertEqual(order.phone, '1234567890')
        self.assertEqual(order.email, 'test@example.com')
        self.assertEqual(order.total, 100.0)
        # Другие ассерты для остальных полей

    def test_order_should_send_email_property(self):
        # Тест для свойства should_send_email
        order1 = Order.objects.create(account=self.account, type_payment='bank', status='stash')
        order2 = Order.objects.create(account=self.account, type_payment='receiving', status='stash')
        order3 = Order.objects.create(account=self.account, type_payment='receiving', status='processing')

        self.assertFalse(order1.should_send_email)
        self.assertTrue(order2.should_send_email)
        self.assertTrue(order3.should_send_email)

    # Другие тесты для методов и свойств модели Order

    def test_order_add_completed_state(self):
        # Тест для метода add_completed_state
        order = Order.objects.create(account=self.account, current_state=self.state)

        self.assertEqual(order.completed_states.count(), 0)

        new_state = OrderState.objects.create(name='New State', code='new')
        order.add_completed_state(new_state)

        self.assertEqual(order.completed_states.count(), 1)
        self.assertEqual(order.completed_states.first(), new_state)

from django.test import TestCase
from apps.shop.models import Order
from filer.models import File
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

class OrderLogModelTestCase(TestCase):

    def setUp(self):
        # Создаем объекты, которые могут понадобиться для тестов
        self.order = Order.objects.create(
            account=None,
            surname='Test',
            name='User',
            email='test@example.com',
            status='processing',
            type_payment='receiving',
            shipping='self',
            shipping_price=0,
            is_confirmed=False,
            current_state=None,
        )

        # Создаем фейковый файл для лога
        file_content = b'This is a test log file content.'
        file = SimpleUploadedFile("test_log.txt", file_content)
        self.log_file = File.objects.create(name="test_log.txt", file=file)


from django.test import TestCase
from apps.shop.models import OrderState

class OrderStateModelTestCase(TestCase):

    def test_order_state_creation(self):
        # Тест на создание объекта OrderState
        order_state = OrderState.objects.create(
            title="Новый статус",
            code="NEW_STATUS_CODE",
            position=2,
        )

        self.assertEqual(order_state.title, "Новый статус")
        self.assertEqual(order_state.code, "NEW_STATUS_CODE")
        self.assertEqual(order_state.position, 2)

    def test_order_state_str_method(self):
        # Тест для метода __str__ модели OrderState
        order_state = OrderState.objects.create(
            title="Новый статус",
            code="NEW_STATUS_CODE",
            position=2,
        )

        expected_str = "Новый статус"
        self.assertEqual(str(order_state), expected_str)

    def test_default_order_state_creation(self):
        # Тест на создание объекта OrderState с кодом по умолчанию
        default_order_state = OrderState.default()
        self.assertEqual(default_order_state.code, OrderState.DEFAULT_CODE)

from django.test import TestCase
from apps.shop.models.shipping import CourierCity

class CourierCityModelTestCase(TestCase):

    def test_courier_city_creation(self):
        # Тест на создание объекта CourierCity
        courier_city = CourierCity.objects.create(name="Новый город")

        self.assertEqual(courier_city.name, "Новый город")

    def test_courier_city_str_method(self):
        # Тест для метода __str__ модели CourierCity
        courier_city = CourierCity.objects.create(name="Новый город")

        expected_str = "Новый город"
        self.assertEqual(str(courier_city), expected_str)




