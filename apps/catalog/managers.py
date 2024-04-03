from django.db import models
from django.db.models import (
    Count,
    Sum,
    Min,
    Case,
    When,
    Value,
    F,
    FloatField,
    IntegerField
)


class CustomQuerySet(models.query.QuerySet):

    def annotate_options(self):
        return (self
            .select_related('thumbnail')
            .prefetch_related('prices')
            .filter(active=True)
            .annotate(
            _min_price=Min(
                Case(
                    When(
                        options__active=True,
                        options__price__gt=0,
                        then=F('options__price')
                    ),
                )
            ),
            _options_exists=Sum(
                Case(
                    When(
                        options__active=True,
                        then=Value(1)
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            _options_stock_exists=Sum(
                Case(
                    When(
                        options__active=True,
                        options__count__gt=0,
                        then=Value(1)
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        )
        )


class ProductManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def annotate_options(self):
        return self.get_queryset().annotate_options()

# class ProductManager(models.Manager):

#     def get_queryset(self):
#         queryset = super(ProductManager, self).get_queryset()
#         queryset = (queryset
#                     .select_related('thumbnail')
#                     .filter(active=True)
#                     .annotate(
#                         _min_price=Min(
#                                     Case(
#                                         When(
#                                             options__active=True,
#                                             options__price__gt=0,
#                                             then=F('options__price')
#                                             ),
#                                         )
#                                     ),
#                         _options_exists=Sum(
#                                         Case(
#                                             When(
#                                                 options__active=True,
#                                                 then=Value(1)
#                                                 ),
#                                             default=Value(0),
#                                             output_field=IntegerField(),
#                                             )
#                                         ),
#                         _options_stock_exists=Sum(
#                                         Case(
#                                             When(
#                                                 options__active=True,
#                                                 options__count__gt=0,
#                                                 then=Value(1)
#                                                 ),
#                                             default=Value(0),
#                                             output_field=IntegerField(),
#                                             )
#                                         )
#                         )
#                     )
#         return queryset
