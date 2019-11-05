class HtmlPages():  # Названия html-файлов без .html
    auth = 'auth'
    reg = 'registration'
    contacts = 'contacts'
    srch_inp = 'base'
    srch_res = 'search_result'
    product = 'product_page'
    prod_edit = 'product_edit'
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
