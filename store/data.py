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
