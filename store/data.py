def getLogger():
    import logging, sys
    logging.basicConfig(format='[%(filename)s] %(message)s', stream=sys.stdout, level=logging.INFO)
    return logging.getLogger()


class HtmlPages():  # Названия html-файлов без .html
    auth = 'login_auth'
    reg = 'login_reg'
    reset = 'login_reset'
    act = 'activate'
    cng = 'change'
    out = 'logout'
    contacts = 'contacts'
    src = 'search'
    prd = 'products'
    ord = 'order'
    ord_add = 'order/add'
    ord_del = 'order/del'
    ord_com = 'complete'
    home = 'home'
    cab = 'cabinet'


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
