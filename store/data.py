def getLogger():
    import logging, sys
    logging.basicConfig(format='[%(filename)s] %(message)s', stream=sys.stdout, level=logging.INFO)
    return logging.getLogger()


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
    edit_all = 'edit_panel'
    edit_prd = 'edit_product'
    edit_cat = 'edit_category'
    edit_bst = 'edit_basket'
    add_prd = 'add_product'
    add_cat = 'add_category'
    add_bst = 'add_basket'


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
