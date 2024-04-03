from django.test import TestCase
from apps.catalog.models import AttributesGroup, AttributeValue, Attribute, NumAttribute
from apps.catalog.models import Product, Category  # Импортируйте ваши модели catalog

class AttributesGroupTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(title="Test Product", category=self.category)

    def test_attributes_group_creation(self):
        group = AttributesGroup.objects.create(
            title="Test Group",
            type_value=0,
            show=True,
            show_parent=True,
            show_in_header=True,
        )
        self.assertIsNotNone(group.id)

    def test_search_attributes(self):
        group = AttributesGroup.objects.create(
            title="Test Group",
            type_value=0,
        )
        attribute_value = AttributeValue.objects.create(title="Test Value")
        attribute = Attribute.objects.create(
            product=self.product,
            group=group,
            value=attribute_value,
        )
        products = [self.product]
        result = group.search_attributes(products)
        self.assertEqual(result['group'], group.title)
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['attributes']), 1)

    def test_search_input_names(self):
        group = AttributesGroup.objects.create(
            title="Test Group",
            type_value=0,
        )
        attribute_value = AttributeValue.objects.create(title="Test Value")
        attribute = Attribute.objects.create(
            product=self.product,
            group=group,
            value=attribute_value,
        )
        products = [self.product]
        result = group.search_input_names(products)
        self.assertEqual(len(result), 1)

    # Добавьте другие тесты для остальных методов и функциональности модели AttributesGroup


class AttributeValueTestCase(TestCase):

    def test_attribute_value_creation(self):
        value = AttributeValue.objects.create(title="Test Value")
        self.assertIsNotNone(value.id)

    # Добавьте другие тесты для остальных методов и функциональности модели AttributeValue


class AttributeTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(title="Test Product", category=self.category)
        self.group = AttributesGroup.objects.create(title="Test Group", type_value=0)
        self.value = AttributeValue.objects.create(title="Test Value")

    def test_attribute_creation(self):
        attribute = Attribute.objects.create(
            product=self.product,
            group=self.group,
            value=self.value,
        )
        self.assertIsNotNone(attribute.id)

    def test_attributes_str(self):
        attribute = Attribute.objects.create(
            product=self.product,
            group=self.group,
            value=self.value,
        )
        expected_str = f"{self.product.title} - {self.group.title} - {self.value.title}"
        self.assertEqual(str(attribute), expected_str)

    # Добавьте другие тесты для остальных методов и функциональности модели Attribute


class NumAttributeTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(title="Test Product", category=self.category)
        self.group = AttributesGroup.objects.create(title="Test Num Group", type_value=1)

    def test_num_attribute_creation(self):
        num_attribute = NumAttribute.objects.create(
            product=self.product,
            group=self.group,
            value=42.0,
        )
        self.assertIsNotNone(num_attribute.id)

    def test_num_attributes_str(self):
        num_attribute = NumAttribute.objects.create(
            product=self.product,
            group=self.group,
            value=42.0,
        )
        expected_str = f"{self.product.title} - {self.group.title} - 42.0"
        self.assertEqual(str(num_attribute), expected_str)

from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Brand, BrandFile
from django.core.files.uploadedfile import SimpleUploadedFile

class BrandTestCase(TestCase):

    def test_brand_creation(self):
        brand = Brand.objects.create(
            title="Test Brand",
            slug="test-brand",
        )
        self.assertIsNotNone(brand.id)

    def test_get_absolute_url(self):
        brand = Brand.objects.create(
            title="Test Brand",
            slug="test-brand",
        )
        expected_url = reverse("brand", kwargs={"slug": brand.slug})
        self.assertEqual(brand.get_absolute_url(), expected_url)

    def test_brand_upperizer(self):
        brand = Brand.objects.create(
            title="Test Brand",
            slug="test-brand",
        )
        self.assertEqual(brand.title_upper, "TEST BRAND")

    # Добавьте другие тесты для остальных методов и функциональности модели Brand


class BrandFileTestCase(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(
            title="Test Brand",
            slug="test-brand",
        )
        # Создание временного файла для тестирования
        uploaded_file = SimpleUploadedFile(
            "test.txt", b"file_content", content_type="text/plain")
        self.brand_file = BrandFile.objects.create(
            brand=self.brand,
            obj=uploaded_file,
            title="Test File",
        )

    def test_brand_file_creation(self):
        self.assertIsNotNone(self.brand_file.id)

    def test_get_type(self):
        self.assertEqual(self.brand_file.get_type(), "txt")

    def test_get_size(self):
        self.assertEqual(self.brand_file.get_size(), "11 Б")


from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Category

class CategoryTestCase(TestCase):

    def setUp(self):
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
            # Добавьте остальные необходимые поля здесь
        )

    def test_category_creation(self):
        self.assertIsNotNone(self.category.id)

    def test_get_absolute_url(self):
        expected_url = reverse("product-category", kwargs={"slug": self.category.slug})
        self.assertEqual(self.category.get_absolute_url(), expected_url)

    def test_get_breadcrumbs(self):
        # Создайте тестовую структуру категорий и убедитесь, что breadcrumbs правильно формируются
        parent_category = Category.objects.create(
            title="Parent Category",
            slug="parent-category",
            parent=None
        )
        self.category.parent = parent_category
        self.category.save()

        breadcrumbs = self.category.get_breadcrumbs()
        self.assertEqual(breadcrumbs[0]["title"], "Главная")
        self.assertEqual(breadcrumbs[1]["title"], "Каталог")
        self.assertEqual(breadcrumbs[2]["title"], "Parent Category")
        self.assertEqual(breadcrumbs[3]["title"], "Test Category")

from django.test import TestCase
from apps.catalog.models import ColorValue, Color, Product

class ColorValueTestCase(TestCase):

    def setUp(self):
        self.color_value = ColorValue.objects.create(
            title="Red",
            hex_color="#FF0000"
        )

    def test_color_value_creation(self):
        self.assertIsNotNone(self.color_value.id)

    def test_color_value_str(self):
        self.assertEqual(str(self.color_value), "Red")

class ColorTestCase(TestCase):

    def setUp(self):
        # Создаем тестовый товар и значение цвета
        self.product = Product.objects.create(
            title="Test Product",
            # Добавьте остальные необходимые поля здесь
        )
        self.color_value = ColorValue.objects.create(
            title="Red",
            hex_color="#FF0000"
        )
        self.color = Color.objects.create(
            product=self.product,
            value=self.color_value,
            price=10.0
        )

    def test_color_creation(self):
        self.assertIsNotNone(self.color.id)

    def test_color_str(self):
        expected_str = "Test Product - Red"
        self.assertEqual(str(self.color), expected_str)

    def test_color_price(self):
        self.assertEqual(self.color.price, 10.0)

    def test_color_product(self):
        self.assertEqual(self.color.product, self.product)

    def test_color_value(self):
        self.assertEqual(self.color.value, self.color_value)


from django.test import TestCase
from apps.catalog.models import Country

class CountryTestCase(TestCase):

    def setUp(self):
        self.country = Country.objects.create(
            title="Test Country"
        )

    def test_country_creation(self):
        self.assertIsNotNone(self.country.id)

    def test_country_str(self):
        self.assertEqual(str(self.country), "Test Country")


from django.test import TestCase
from apps.catalog.models import Direction

class DirectionTestCase(TestCase):

    def setUp(self):
        self.direction = Direction.objects.create(
            title="Test Direction",
            title_original="Original Title",
            mobile_title="Mobile Title",
            black_color=True,
            sort=100
        )

    def test_direction_creation(self):
        self.assertIsNotNone(self.direction.id)

    def test_direction_str(self):
        self.assertEqual(str(self.direction), "Test Direction")

    def test_get_title(self):
        self.assertEqual(self.direction.get_title(), "Original Title")

    def test_get_mobile_title(self):
        self.assertEqual(self.direction.get_mobile_title(), "Mobile Title")

    def test_get_mobile_thumbnail(self):
        self.assertEqual(self.direction.get_mobile_thumbnail(), self.direction.mobile_thumbnail)

    def test_sort_field(self):
        self.assertEqual(self.direction.sort, 100)

    def test_black_color_field(self):
        self.assertTrue(self.direction.black_color)


from django.test import TestCase
from apps.catalog.models import IndexBlock

class IndexBlockTestCase(TestCase):

    def setUp(self):
        self.index_block = IndexBlock.objects.create(
            title="Test Block",
            href="/test/",
            is_active=True,
            is_clickable=True
        )

    def test_index_block_creation(self):
        self.assertIsNotNone(self.index_block.id)

    def test_index_block_str(self):
        self.assertEqual(str(self.index_block), "Test Block")

    def test_is_active_field(self):
        self.assertTrue(self.index_block.is_active)

    def test_is_clickable_field(self):
        self.assertTrue(self.index_block.is_clickable)

    def test_href_field(self):
        self.assertEqual(self.index_block.href, "/test/")

    def test_image_right_bottom_field(self):
        self.assertIsNone(self.index_block.image_right_bottom)

    def test_image_right_top_field(self):
        self.assertIsNone(self.index_block.image_right_top)

    def test_image_left_bottom_field(self):
        self.assertIsNone(self.index_block.image_left_bottom)



from django.test import TestCase
from apps.catalog.models import Option, Product

class OptionTestCase(TestCase):

    def setUp(self):
        # Создаем продукт, который будет связан с опцией
        self.product = Product.objects.create(title="Test Product")
        self.option = Option.objects.create(
            product=self.product,
            unloading_id="1",
            active=True,
            title="Test Option",
            step=1,
            count=10,
            price=25.0
        )

    def test_option_creation(self):
        self.assertIsNotNone(self.option.id)

    def test_option_str(self):
        self.assertEqual(str(self.option), "Test Option")

    def test_active_field(self):
        self.assertTrue(self.option.active)

    def test_title_field(self):
        self.assertEqual(self.option.title, "Test Option")

    def test_step_field(self):
        self.assertEqual(self.option.step, 1)

    def test_count_field(self):
        self.assertEqual(self.option.count, 10)

    def test_price_field(self):
        self.assertEqual(self.option.price, 25.0)

    def test_default_price_property(self):
        self.assertEqual(self.option.default_price, 25.0)


from django.test import TestCase
from apps.catalog.models import PriceType, ProductPrice, OptionPrice, get_default_price_type

class PriceTypeTestCase(TestCase):

    def setUp(self):
        self.price_type = PriceType.objects.create(
            id_1c="RETAIL", title="Retail Price"
        )

    def test_price_type_creation(self):
        self.assertIsNotNone(self.price_type.id)

    def test_price_type_str(self):
        self.assertEqual(str(self.price_type), "Retail Price")

    def test_get_by_title_existing(self):
        price_type = PriceType.get_by_title("Retail Price")
        self.assertEqual(price_type, self.price_type)

    def test_get_by_title_non_existing(self):
        price_type = PriceType.get_by_title("Non-existing Price")
        self.assertIsNone(price_type)

class ProductPriceTestCase(TestCase):

    def setUp(self):
        self.price_type = PriceType.objects.create(
            id_1c="RETAIL", title="Retail Price"
        )
        self.product = Product.objects.create(title="Test Product")
        self.product_price = ProductPrice.objects.create(
            type=self.price_type, product=self.product, value=25.0
        )

    def test_product_price_creation(self):
        self.assertIsNotNone(self.product_price.id)

    def test_product_price_str(self):
        self.assertEqual(str(self.product_price), "Test Product")

class OptionPriceTestCase(TestCase):

    def setUp(self):
        self.price_type = PriceType.objects.create(
            id_1c="RETAIL", title="Retail Price"
        )
        self.option = Option.objects.create(
            product=None, unloading_id="1", active=True, title="Test Option", step=1, count=10, price=25.0
        )
        self.option_price = OptionPrice.objects.create(
            type=self.price_type, option=self.option, value=30.0
        )

    def test_option_price_creation(self):
        self.assertIsNotNone(self.option_price.id)

    def test_option_price_str(self):
        self.assertEqual(str(self.option_price), "Test Option")

class GetDefaultPriceTypeTestCase(TestCase):

    def test_default_price_type_exists(self):
        price_type = get_default_price_type()
        self.assertIsNotNone(price_type)

    def test_default_price_type_non_existing(self):
        # Удаляем существующий тип цены, чтобы тестировать создание нового
        PriceType.objects.filter(id_1c="RETAIL").delete()
        price_type = get_default_price_type()
        self.assertIsNotNone(price_type)


from django.test import TestCase
from apps.catalog.models import Product, Category, Direction, Brand
from django.urls import reverse

class ProductTestCase(TestCase):

    def setUp(self):
        # Создаем необходимые объекты для тестов
        self.category = Category.objects.create(title="Test Category")
        self.direction = Direction.objects.create(title="Test Direction")
        self.brand = Brand.objects.create(title="Test Brand")

        self.product = Product.objects.create(
            title="Test Product",
            category=self.category,
            price=100.0,
            count=10,
            brand=self.brand,
            directions=[self.direction],
            sale=False,
            active=True
        )

    def test_product_creation(self):
        self.assertIsNotNone(self.product.id)

    def test_product_absolute_url(self):
        url = reverse('product', kwargs={'slug': self.product.slug})
        self.assertEqual(self.product.get_absolute_url(), url)

    def test_product_display_price(self):
        self.assertTrue(self.product.display_price)
        self.product.sale = True
        self.product.count = 0
        self.assertFalse(self.product.display_price)

    def test_product_default_price(self):
        self.assertEqual(self.product.default_price, 100.0)

    # Продолжите создавать другие тесты для остальных методов вашей модели.
    # Не забудьте также создать тесты для методов, которые зависят от пользователя (user).

    def test_product_min_price(self):
        # Создайте тесты для метода min_price
        pass

    def test_product_has_count(self):
        # Создайте тесты для метода has_count
        pass

    def test_product_is_shock_sale(self):
        # Создайте тесты для метода is_shock_sale
        pass

    def test_product_get_status(self):
        # Создайте тесты для метода get_status
        pass

    def test_product_get_similar_items(self):
        # Создайте тесты для метода get_similar_items
        pass

    def test_product_get_filters(self):
        # Создайте тесты для метода get_filters
        pass


from django.test import TestCase
from apps.catalog.models import ProductStorage, ProductStorageCount, Product, Option
from django.db.utils import IntegrityError

class ProductStorageCountTestCase(TestCase):

    def setUp(self):
        # Создаем необходимые объекты для тестов
        self.storage = ProductStorage.objects.create(
            upload_title="Test Storage", title="Test Storage")
        self.product = Product.objects.create(
            title="Test Product", price=100.0, count=0)
        self.option = Option.objects.create(
            title="Test Option", price=50.0, count=0)

    def test_product_storage_count_creation(self):
        # Проверяем создание объекта ProductStorageCount
        count = ProductStorageCount.objects.create(
            product=self.product, storage=self.storage, count=10)
        self.assertIsNotNone(count.id)

        # Проверяем создание объекта ProductStorageCount с вариативным товаром
        count_option = ProductStorageCount.objects.create(
            option=self.option, storage=self.storage, count=5)
        self.assertIsNotNone(count_option.id)

    def test_set_total_count_instance(self):
        # Проверяем обновление общего количества товара после создания ProductStorageCount
        self.product.count = 0
        self.product.save()

        count = ProductStorageCount.objects.create(
            product=self.product, storage=self.storage, count=10)
        self.assertEqual(self.product.count, 10)

        count.count = 15
        count.save()
        self.assertEqual(self.product.count, 15)

        # Проверяем обновление общего количества вариативного товара после создания ProductStorageCount
        self.option.count = 0
        self.option.save()

        count_option = ProductStorageCount.objects.create(
            option=self.option, storage=self.storage, count=5)
        self.assertEqual(self.option.count, 5)

        count_option.count = 8
        count_option.save()
        self.assertEqual(self.option.count, 8)

