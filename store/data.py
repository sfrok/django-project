def getLogger():
    import logging, sys
    logging.basicConfig(format='[%(filename)s] %(message)s', stream=sys.stdout, level=logging.INFO)
    return logging.getLogger()


class HtmlPages():  # Названия html-файлов без .html
    auth = 'login_auth'
    reg = 'login_reg'
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
    add_prd = 'edit_product_add'
    add_cat = 'edit_category_add'
    add_bst = 'edit_basket_add'


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
