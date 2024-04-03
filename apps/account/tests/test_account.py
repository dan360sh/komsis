from django.test import TestCase
from django.contrib.auth.models import User
from apps.account.models import Account, AccountStatus, DiscountCard


class AccountTestCase(TestCase):

    def setUp(self):
        # Создаем несколько объектов, которые могут быть необходимы для тестов
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.account_status = AccountStatus.objects.create(
            title='New Status', min_limit=0, max_limit=100)
        self.discount_card = DiscountCard.objects.create(
            title='Gold Card', percent=15.0, id_1c='123456')

    def test_account_creation(self):
        account = Account.objects.create(
            user=self.user,
            email='test@example.com',
            name='John',
            surname='Doe',
            middle_name='Smith',
            phone='1234567890',
            valid_phone='1234567890',
            status=self.account_status,
            discount_card=self.discount_card,
        )
        self.assertIsNotNone(account.id)

    def test_count_points(self):
        account = Account.objects.create(
            user=self.user,
            email='test@example.com',
            name='John',
            surname='Doe',
            middle_name='Smith',
            phone='1234567890',
            valid_phone='1234567890',
            status=self.account_status,
            discount_card=self.discount_card,
        )
        purchase_cost = 100.0
        expected_points = 15.0  # 15% of 100.0
        self.assertEqual(account.count_points(purchase_cost), expected_points)

    def test_calculate_discount(self):
        account = Account.objects.create(
            user=self.user,
            email='test@example.com',
            name='John',
            surname='Doe',
            middle_name='Smith',
            phone='1234567890',
            valid_phone='1234567890',
            status=self.account_status,
            discount_card=self.discount_card,
        )
        purchase_cost = 100.0
        points = 15.0
        expected_discount = 85.0  # 100.0 - 15.0
        self.assertEqual(account.calculate_discount(purchase_cost, points), expected_discount)

    # Добавьте другие тесты для остальных методов и функциональности модели

    def test_get_clear_name(self):
        account = Account.objects.create(
            user=self.user,
            email='test@example.com',
            name='John',
            surname='Doe',
            middle_name='Smith',
            phone='1234567890',
            valid_phone='1234567890',
            status=self.account_status,
            discount_card=self.discount_card,
        )
        expected_clear_name = 'Doe John Smith'
        self.assertEqual(account.get_clear_name(account), expected_clear_name)


from django.test import TestCase
from apps.account.models import DiscountCard


class DiscountCardTestCase(TestCase):

    def setUp(self):
        self.discount_card = DiscountCard.objects.create(
            title='Silver Card',
            percent=10.0,
            id_1c='12345'
        )

    def test_discount_card_creation(self):
        self.assertIsNotNone(self.discount_card.id)

    def test_discount_card_str_method(self):
        self.assertEqual(str(self.discount_card), 'Silver Card')

    def test_get_discount_property(self):
        self.assertEqual(self.discount_card.get_discount, 0.1)

    def test_unique_id_1c(self):
        # Попробуйте создать другую карту с тем же id_1c
        with self.assertRaises(Exception):
            DiscountCard.objects.create(
                title='Gold Card',
                percent=15.0,
                id_1c='12345'
            )


from django.test import TestCase
from apps.account.models import Manager


class ManagerTestCase(TestCase):

    def setUp(self):
        self.manager = Manager.objects.create(
            name='John Doe',
            phone='1234567890',
            email='john@example.com'
        )

    def test_manager_creation(self):
        self.assertIsNotNone(self.manager.id)

    def test_manager_str_method(self):
        self.assertEqual(str(self.manager), 'John Doe')


from django.test import TestCase
from apps.account.models import AccountStatus


class AccountStatusTestCase(TestCase):

    def setUp(self):
        self.account_status = AccountStatus.objects.create(
            title='Test Status',
            min_limit=0,
            max_limit=1000
        )

    def test_account_status_creation(self):
        self.assertIsNotNone(self.account_status.id)

    def test_account_status_str_method(self):
        self.assertEqual(str(self.account_status), 'Test Status')

    def test_account_status_default_method(self):
        default_status = AccountStatus.default()
        self.assertIsNotNone(default_status)

    def test_account_status_get_next(self):
        next_status = AccountStatus.objects.create(
            title='Next Status',
            min_limit=1001,
            max_limit=2000,
            previous_status=self.account_status
        )
        self.assertEqual(self.account_status.get_next(), next_status)
        self.assertIsNone(next_status.get_next())

    def test_account_status_is_last(self):
        self.assertFalse(self.account_status.is_last)

    def test_account_status_is_last_with_null_max_limit(self):
        status = AccountStatus.objects.create(
            title='Null Max Limit Status',
            min_limit=0,
            max_limit=None
        )
        self.assertTrue(status.is_last)

    def test_account_status_is_last_with_zero_max_limit(self):
        status = AccountStatus.objects.create(
            title='Zero Max Limit Status',
            min_limit=0,
            max_limit=0
        )
        self.assertTrue(status.is_last)
