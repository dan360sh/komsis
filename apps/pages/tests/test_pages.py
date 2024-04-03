from django.test import TestCase
from django.urls import reverse
from apps.pages.models import Offer
from datetime import date

class OfferTestCase(TestCase):

    def setUp(self):
        # Создаем объект Offer для использования в тестах
        self.offer = Offer.objects.create(
            active=True,
            title='Тестовая акция',
            description='Описание тестовой акции',
            slug='test-offer',
            date=date.today(),
        )

    def test_offer_creation(self):
        # Проверяем, что объект Offer был создан корректно
        self.assertEqual(self.offer.active, True)
        self.assertEqual(self.offer.title, 'Тестовая акция')
        self.assertEqual(self.offer.description, 'Описание тестовой акции')
        self.assertEqual(self.offer.slug, 'test-offer')
        self.assertEqual(self.offer.date, date.today())

    def test_get_absolute_url(self):
        # Проверяем, что метод get_absolute_url возвращает правильный URL
        expected_url = reverse('offer', kwargs={'slug': 'test-offer'})
        self.assertEqual(self.offer.get_absolute_url(), expected_url)

    def test_offer_update(self):
        # Обновляем объект Offer и проверяем, что изменения сохраняются
        self.offer.title = 'Обновленная акция'
        self.offer.save()
        updated_offer = Offer.objects.get(pk=self.offer.pk)
        self.assertEqual(updated_offer.title, 'Обновленная акция')

    def test_offer_deletion(self):
        # Удаляем объект Offer и проверяем, что он больше не существует
        offer_id = self.offer.pk
        self.offer.delete()
        with self.assertRaises(Offer.DoesNotExist):
            deleted_offer = Offer.objects.get(pk=offer_id)


from django.test import TestCase
from django.urls import reverse
from apps.pages.models import Page
from datetime import date

class PageTestCase(TestCase):

    def setUp(self):
        # Создаем объект Page для использования в тестах
        self.page = Page.objects.create(
            active=True,
            title='Тестовая страница',
            slug='test-page',
            template=0,  # Вы можете выбрать нужный шаблон
        )

    def test_page_creation(self):
        # Проверяем, что объект Page был создан корректно
        self.assertEqual(self.page.active, True)
        self.assertEqual(self.page.title, 'Тестовая страница')
        self.assertEqual(self.page.slug, 'test-page')
        self.assertEqual(self.page.template, 0)  # Проверьте выбранный шаблон

    def test_get_absolute_url(self):
        # Проверяем, что метод get_absolute_url возвращает правильный URL
        expected_url = reverse('page', kwargs={'slug': 'test-page'})
        self.assertEqual(self.page.get_absolute_url(), expected_url)

    def test_page_update(self):
        # Обновляем объект Page и проверяем, что изменения сохраняются
        self.page.title = 'Обновленная страница'
        self.page.save()
        updated_page = Page.objects.get(pk=self.page.pk)
        self.assertEqual(updated_page.title, 'Обновленная страница')

    def test_page_deletion(self):
        # Удаляем объект Page и проверяем, что он больше не существует
        page_id = self.page.pk
        self.page.delete()
        with self.assertRaises(Page.DoesNotExist):
            deleted_page = Page.objects.get(pk=page_id)

from django.test import TestCase
from apps.pages.models import Vacancy

class VacancyTestCase(TestCase):

    def test_vacancy_creation(self):
        # Проверяем, что объект Vacancy был создан корректно
        self.assertEqual(self.vacancy.title, 'Тестовая вакансия')
        self.assertEqual(self.vacancy.text, 'Текст тестовой вакансии')
        self.assertEqual(self.vacancy.sort, 1)
        self.assertEqual(self.vacancy.city, self.city)

    def test_vacancy_update(self):
        # Обновляем объект Vacancy и проверяем, что изменения сохраняются
        self.vacancy.title = 'Обновленная вакансия'
        self.vacancy.save()
        updated_vacancy = Vacancy.objects.get(pk=self.vacancy.pk)
        self.assertEqual(updated_vacancy.title, 'Обновленная вакансия')

    def test_vacancy_deletion(self):
        # Удаляем объект Vacancy и проверяем, что он больше не существует
        vacancy_id = self.vacancy.pk
        self.vacancy.delete()
        with self.assertRaises(Vacancy.DoesNotExist):
            deleted_vacancy = Vacancy.objects.get(pk=vacancy_id)

