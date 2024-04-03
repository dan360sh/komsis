from typing import Any, Optional

from apps.catalog.models import Category, Product
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.db.models import QuerySet
from requests import delete
from slugify import slugify


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        categories: QuerySet[Category] = Category.objects.all()
        for elem in categories:
            try:
                if elem.parent is None:
                    elem.slug = slugify(elem.title)
                    elem.save()
                    continue
                elem.slug = slugify(elem.title + elem.parent.title)
                elem.save()
            except IntegrityError as err:
                print(err)
                elem.delete()
        products: QuerySet[Product] = Product.objects.all()
        for product in products:
            try:
                if product.code:
                    product.slug = slugify(product.title + product.code)
                    product.save()
                    continue
                if product.category is None:
                    continue
                product.slug = slugify(product.title + product.category.title)
                product.save()
            except IntegrityError as err:
                print(err)
                product.delete()
