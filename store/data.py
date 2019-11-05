CATEGORIES = (
    (None, '...'),
    ('cat_1', 'Категория 1'),
    ('cat_2', 'Категория 2'),
    ('cat_3', 'Категория 3'),
    ('cat_4', 'Категория 4'),
)


class HtmlPages():  # Названия html-файлов без .html
    auth = 'auth'
    reg = 'registration'
    contacts = 'contacts'
    srch_inp = 'base'
    srch_res = 'search_result'
    product = 'product_page'
    ord = 'order'
    ord_com = 'order_complete'
    settings = 'settings'
    ord_list = 'order_list'
    home = 'base'


SELL_STATES = (
    (0, 'Есть в наличии'),
    (1, 'Нет в наличии'),
    (2, 'На заказ'),
)


STATUSES = (
    (0, 'Заказ оплачен'),
    (1, 'Товар отправлен'),
    (2, 'Товар доставлен'),
)
