class Pagin():
    def __init__(self, items, prev, page, pages, last, next):
        self.items = items
        self.prev = prev
        self.pages = pages
        self.next = next
        self.last = last
        self.page = page
        self.count_minus = len(self.pages) - 1
        if 1 not in self.pages:
            self.first = True


def pagination(items, page, count_in_page):
    if not items:
        return False
    page = int(page)
    count_in_page = int(count_in_page)
    ost = items.count() % count_in_page
    if ost == 0:
        count_pages = items.count() // count_in_page + 1
    else:
        count_pages = items.count() // count_in_page + 2
    pages = range(1, count_pages)
    if page > pages[-1]:
        page = 1

    work_page = page - 1

    pages_on_page = []

    if page < 5:
        start = 1
        finish = 6
    elif page > pages[-1] - 3:
        start = pages[-1] - 4
        finish = pages[-1] + 1
    else:
        start = page - 2
        finish = start + 5

    pages_on_page = pages[start - 1:finish - 1]

    if pages[0] in pages_on_page:
        first = False
    else:
        first = pages[0]

    if pages[-1] in pages_on_page:
        last = False
    else:
        last = pages[-1]

    if page <= 1:
        prev = False
    else:
        prev = page - 1

    if page >= len(pages):
        next = False
    else:
        next = page + 1
    return Pagin(
        items[
            (page - 1) * count_in_page: (page - 1) * count_in_page + count_in_page
        ], prev, page, pages_on_page, last, next)
