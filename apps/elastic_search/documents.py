from django_elasticsearch_dsl import Document, fields  # , analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from apps.catalog.models import Product, Brand, Attribute, Category
from .elastic_search import fuzzy_analyzer, en_rus_analyzer

"""
Если в поле нужно поменять анализатор или какой-либо параметр, 
 то он прописывается как атрибут докумена.
Если индексация поля нужна по стандартным алгоритмам,
 то можно прописать в Meta: fields.
"""

@registry.register_document
class ProductDocument(Document):
    # title = fields.TextField(analyzer="russian")
    # title_upper = fields.TextField(analyzer="russian")
    title = fields.TextField(attr="title", analyzer=en_rus_analyzer)
    title_upper = fields.TextField(analyzer=en_rus_analyzer)
    description = fields.TextField(attr="description", analyzer="russian")
    category_root = fields.TextField(attr="get_root_category_title", analyzer=en_rus_analyzer)
    category_root_id = fields.IntegerField(attr="get_root_category_id")
    slug = fields.TextField(attr="slug")
    # поля количество
    countVologda = fields.FloatField(attr="get_count_vologda")
    countCherepovets = fields.FloatField(attr="get_count_cherepovets")
    # counts = fields.ObjectField(
    #     properties={
    #         "countVologda": fields.FloatField(attr="get_count_vologda"),
    #         "countCherepovets": fields.FloatField(attr="get_count_cherepovets")
    #     }
    # )
    # поля фк
    category = fields.ObjectField(
        properties={
            "title": fields.TextField(),
        }
    )
    brand = fields.ObjectField(
        properties={
            "title": fields.TextField(),
            "text": fields.TextField(analyzer="russian"),
        }
    )
    # поля обратные фк
    product_attrbutes = fields.NestedField(properties={
        # 'pk': fields.IntegerField(),
        'group_id': fields.IntegerField(),
        'value_id': fields.IntegerField(),
        'name': fields.TextField(),
    }, include_in_root=True)

    sort = fields.IntegerField()

    related_models = [Attribute]

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related("brand", "category").prefetch_related("product_attrbutes")

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Brand):
            return related_instance.brand
        elif isinstance(related_instance, Category):
            return related_instance.category
        elif isinstance(related_instance, Attribute):
            return related_instance.product_attrbutes.all()

    class Index:
        name = "products"

    class Django:
        model = Product

        fields = [
            "price",
            "code",
        ]
