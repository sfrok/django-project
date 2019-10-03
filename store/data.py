CATEGORIES = (
        ('tech', 'Категория 1'),
        ('toys', 'Категория 2'),
        ('food', 'Категория 3'),
        ('food', 'Категория 4'),
        ('none', 'Пусто'),
    )

class HtmlPages(): # Названия html-файлов без .html
    auth = 'auth'
    reg = 'registration'
    contacts = 'contacts'
    search_input = 'base'
    search_result = 'search_result'
    product_page = 'product_page'

SELL_STATES = (
        (0, 'Есть в наличии'),
        (1, 'Нет в наличии'),
        (2, 'На заказ'),
    )