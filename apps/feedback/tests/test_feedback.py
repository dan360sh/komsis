from django.test import TestCase
from apps.feedback.models import Email, serviceEmail, LoggingEmail
from django.core.exceptions import ValidationError
from datetime import datetime

class EmailTestCase(TestCase):

    def test_email_creation(self):
        # Создаем объект email
        email = Email.objects.create(
            title='example@example.com'
        )

        # Проверяем, что объект email был создан корректно
        self.assertEqual(email.title, 'example@example.com')

    def test_email_string_representation(self):
        # Создаем объект email
        email = Email.objects.create(
            title='example@example.com'
        )

        # Проверяем, что строковое представление объекта email корректно
        self.assertEqual(str(email), 'example@example.com')

class ServiceEmailTestCase(TestCase):

    def test_service_email_creation(self):
        # Создаем объект serviceEmail
        service_email = serviceEmail.objects.create(
            title='service@example.com',
            subscription_exchange=True
        )

        # Проверяем, что объект serviceEmail был создан корректно
        self.assertEqual(service_email.title, 'service@example.com')
        self.assertTrue(service_email.subscription_exchange)

    def test_service_email_string_representation(self):
        # Создаем объект serviceEmail
        service_email = serviceEmail.objects.create(
            title='service@example.com',
            subscription_exchange=True
        )

        # Проверяем, что строковое представление объекта serviceEmail корректно
        self.assertEqual(str(service_email), 'service@example.com')

class LoggingEmailTestCase(TestCase):

    def test_logging_email_creation(self):
        # Создаем объект LoggingEmail
        logging_email = LoggingEmail.objects.create(
            date=datetime.now(),
            to='recipient@example.com',
            subject='Test Email',
            ok=True,
            exception_body='No exceptions',
            result='Success'
        )

        # Проверяем, что объект LoggingEmail был создан корректно
        self.assertEqual(logging_email.to, 'recipient@example.com')
        self.assertEqual(logging_email.subject, 'Test Email')
        self.assertTrue(logging_email.ok)
        self.assertEqual(logging_email.exception_body, 'No exceptions')
        self.assertEqual(logging_email.result, 'Success')

    def test_logging_email_string_representation(self):
        # Создаем объект LoggingEmail
        logging_email = LoggingEmail.objects.create(
            date=datetime.now(),
            to='recipient@example.com',
            subject='Test Email',
            ok=True,
            exception_body='No exceptions',
            result='Success'
        )

        # Проверяем, что строковое представление объекта LoggingEmail корректно
        self.assertEqual(str(logging_email), 'Test Email')

    def test_set_error_body(self):
        # Создаем объект LoggingEmail
        logging_email = LoggingEmail.objects.create(
            date=datetime.now(),
            to='recipient@example.com',
            subject='Test Email',
            ok=True,
            exception_body=None,
            result=None
        )

        # Создаем исключение и вызываем метод set_error_body
        exception = ValidationError('Test Exception')
        logging_email.set_error_body(exception)

        # Проверяем, что поле exception_body было заполнено
        self.assertIsNotNone(logging_email.exception_body)


from django.test import TestCase
from apps.feedback.models import Lead

class LeadTestCase(TestCase):

    def setUp(self):
        # Создаем объект Lead для использования в тестах
        self.lead = Lead.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            message='Hello, world!'
        )

    def test_lead_creation(self):
        # Проверяем, что объект Lead был создан корректно
        self.assertEqual(self.lead.name, 'John Doe')
        self.assertEqual(self.lead.email, 'johndoe@example.com')
        self.assertEqual(self.lead.message, 'Hello, world!')

    def test_lead_string_representation(self):
        # Проверяем, что строковое представление объекта Lead корректно
        expected_string = 'John Doejohndoe@example.com'
        self.assertEqual(str(self.lead), expected_string)

    def test_lead_update(self):
        # Обновляем атрибуты объекта Lead
        self.lead.name = 'Jane Smith'
        self.lead.email = 'janesmith@example.com'
        self.lead.message = 'Updated message'
        self.lead.save()

        # Проверяем, что объект был успешно обновлен
        updated_lead = Lead.objects.get(pk=self.lead.pk)
        self.assertEqual(updated_lead.name, 'Jane Smith')
        self.assertEqual(updated_lead.email, 'janesmith@example.com')
        self.assertEqual(updated_lead.message, 'Updated message')

    def test_lead_deletion(self):
        # Удаляем объект Lead
        lead_id = self.lead.pk
        self.lead.delete()

        # Проверяем, что объект был успешно удален
        with self.assertRaises(Lead.DoesNotExist):
            deleted_lead = Lead.objects.get(pk=lead_id)

from django.contrib.auth.models import User
from django.test import TestCase
from apps.feedback.models import Subscriber

class SubscriberTestCase(TestCase):

    def setUp(self):
        # Создаем объект User и связанный с ним объект Subscriber
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.subscriber = Subscriber.objects.create(user=self.user)

    def test_subscriber_creation(self):
        # Проверяем, что объект Subscriber был создан корректно
        self.assertEqual(self.subscriber.user, self.user)

    def test_subscriber_deletion(self):
        # Удаляем объект Subscriber
        subscriber_id = self.subscriber.pk
        self.subscriber.delete()

        # Проверяем, что объект Subscriber был успешно удален
        with self.assertRaises(Subscriber.DoesNotExist):
            deleted_subscriber = Subscriber.objects.get(pk=subscriber_id)

    def test_user_deletion_cascades_to_subscriber(self):
        # Удаляем объект User, что должно вызвать каскадное удаление объекта Subscriber
        user_id = self.user.pk
        self.user.delete()

        # Проверяем, что объект User и Subscriber были успешно удалены
        with self.assertRaises(User.DoesNotExist):
            deleted_user = User.objects.get(pk=user_id)

        with self.assertRaises(Subscriber.DoesNotExist):
            deleted_subscriber = Subscriber.objects.get(user_id=user_id)
