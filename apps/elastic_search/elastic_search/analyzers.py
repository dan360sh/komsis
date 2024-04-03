from elasticsearch_dsl import analyzer, tokenizer, analysis
from .keyboard_mapping import mappings


# фильтр очищающий от русскоязычных предлогов, союзов и др. стоп-слов
russian_stop = analysis.token_filter("russian_stop", type="stop", stopwords="_russian_")

# дополнительный фильтр русских слов(слова "для" почему-то нет)
russian_custom_stop = analysis.token_filter("russian_custom_stop", type="stop", stopwords=['для', 'lkz'])

# фильтр оставляющий лишь основу слова "трубчаты -> труб"
russian_stemmer = analysis.token_filter(
    "russian_stemmer", type="stemmer", language="russian"
)
# фильтр для соотвествия русской и английской раскладок
en_rus_key = analysis.char_filter("en_r", type="mapping", mappings=mappings)


# анализатор для нечеткого поиска
fuzzy_analyzer = analyzer(
    "fuzzy_analyzer",
    tokenizer=tokenizer("trigram", "edge_ngram", min_gram=1, max_gram=20),
    filter=["lowercase", russian_stop, russian_stemmer],
    # char_filter=[en_rus_key],
)

# анализатор для различной раскладки клавиатуры
en_rus_analyzer = analyzer(
    "en_rus_analyzer",
    tokenizer="standard",
    filter=["lowercase", russian_stop, russian_custom_stop, russian_stemmer],
    char_filter=[en_rus_key],
)
