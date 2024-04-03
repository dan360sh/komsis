from elasticsearch_dsl.query import Q, MultiMatch, Match, SF
from .documents import ProductDocument


def search(q):
    search = ProductDocument.search()
    search = search.query(
        Q("match", title=q) | Q("match", description=q) | Q("term", code=q)
    )

    query = Q("bool", should=[Q("match", title=q), Q("match", description=q)])
    # match = MultiMatch(fields=["title", "description", "title_upper"], query=q)
    # search = search.query(match)
    # search = search.filter(
    #     "nested",
    #     path="brand",
    #     query=Q("match", brand__title=q) | Q("match", brand__text=q),
    # )
    return search


def get_search_query(phrase):
    # query = MultiMatch(
    #     query=phrase,
    #     # fields=["title", "description", "brand__title", "brand__text"],
    #     fields=["brand__title", "brand__text"],
    #     fuzziness="AUTO",
    # )
    query = Q(Match(title={"query": phrase, "boost": "1", "fuzziness": "AUTO"}))
    query = query | Q(
        Match(description={"query": phrase, "boost": "0.7", "fuzziness": "AUTO"})
    )
    # query = query | Q("nested", path="brand", query=Q("match", brand__title=phrase))
    qm = {
        "brand.text": {"query": phrase, 'boost': '0.3'}
        }
    query = query | Q(Match(**qm))
    query = query | Q(Match(brand__title={"query": phrase, "boost": "0.5"}))
    return ProductDocument.search().query(query)


def search1(phrase):
    response = get_search_query(phrase)
    print(response.to_dict())
    return response.to_queryset(), response


def search_ids(phrase, limit=2000):
    response = get_search_query(phrase)[:limit]
    print(response.to_dict())
    return response.to_queryset()