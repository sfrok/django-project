def getLogger():
    import logging, sys
    logging.basicConfig(format='[%(filename)s] %(message)s', stream=sys.stdout, level=logging.INFO)
    return logging.getLogger()


class HtmlPages():  # Названия html-файлов без .html
    auth = 'login_auth'
    reg = 'login_reg'
    out = 'logout'
    contacts = 'contacts'
    src = 'search'
    product = 'product'
    ord = 'order'
    ord_add = 'order/add'
    ord_del = 'order/del'
    ord_com = 'complete'
    settings = 'settings'
    ord_list = 'basket'
    home = 'home'


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
