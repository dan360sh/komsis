from elasticsearch_dsl.query import SF, Match, MultiMatch, Q

from .documents import ProductDocument
from apps.catalog.models import Product


def get_search_query(phrase):
    query = Match(code={"query": phrase, "boost": "1"})
    query = query | Match(title_upper={"query": phrase, "boost": "4"})
    query = query | Match(
        title={"query": phrase, "boost": "6", "fuzziness": "AUTO:7,9"})
    query = query | Match(category_root={"query": phrase,
                                          "boost": "5", "fuzziness": "AUTO:4,6"})
    query = query | Match(brand__title={"query": phrase, "boost": '3'})
    print(query)
    return ProductDocument.search().query(query)


def search_elastic(phrase, limit=2000, sort_fields=None):
    response = get_search_query(phrase)[:limit]
    if sort_fields:
        response = response.sort(*sort_fields)
    return response


def search_elastic_queryset(phrase, limit=2000, sort_fields=None):
    return search_elastic(phrase, limit, sort_fields).to_queryset()
