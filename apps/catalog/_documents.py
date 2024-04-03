from django_elasticsearch_dsl import Document, fields  # , analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from .models import Product, Brand, Attribute, Category
from .elastic_search import fuzzy_analyzer, en_rus_analyzer


@registry.register_document
class ProductDocument(Document):
    # title = fields.TextField(analyzer="russian")
    # title_upper = fields.TextField(analyzer="russian")
    title = fields.TextField(attr="title", analyzer=en_rus_analyzer)
    title_upper = fields.TextField(analyzer=en_rus_analyzer)
    description = fields.TextField(attr="description", analyzer="russian")
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

    product_attrbutes = fields.NestedField(properties={
        # 'pk': fields.IntegerField(),
        'group_id': fields.IntegerField(),
        'value_id': fields.IntegerField(),
        'name': fields.TextField(),
    }, include_in_root=True)

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
            # "title_upper",
            "code",
        ]
