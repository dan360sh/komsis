from django.template.defaultfilters import slugify as django_slugify

SYMBOLS = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya'
}


def slugify(slug):
    return django_slugify(''.join(SYMBOLS.get(w, w) for w in slug.lower()))


def unique_slugify(title, obj):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while obj.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug
