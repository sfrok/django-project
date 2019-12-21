from django.forms import model_to_dict
from store.data import getLogger
from .models import Product, SingleOrder


def log(*info): getLogger().info(' '.join(info))  # Ф-ия логирования


def search(cat=None, line='', sort_attr='sold'):  # Поиск товаров
    response = Product.objects.filter(name__icontains=line)  # Фильтр по имени
    if cat: 
        response = response.filter(category_id=cat.id)  # По категории
    response = response.order_by(sort_attr)  # Сортировка
    return response


def add_order(request):  # Добавление товара в корзину
    product = Product.objects.get(id=int(request.POST['pid']))  # Товар
    amount = int(request.POST['product_count'])  # Количество
    orders = request.session.get('bcont', [])  # Корзина
    order_exists = False
    for item in orders:  # Обновление товара в корзине, если он там уже есть
        if item['product'] == product.id:
            item['amount'] += amount
            item['sum_price'] += float(amount * product.price)
            order_exists = True
            break
    if not order_exists:  # Добавление товара в корзину, если его там еще нет
        order = model_to_dict(SingleOrder(product=product, amount=amount))
        order.update({'sum_price': float(amount * product.price), 'id': len(orders)})
        orders.append(order)
    request.session['bcont'] = orders  # Сохранение обновленной корзины в сессию


def session_clear(func):  # Декоратор логирования и удаления сессионных переменных
    def wrapper(request, *args):
        session_vars = [f'{k}:{v}' for k, v in request.session.items() if len(k) < 6]
        if session_vars: log("session:", ',\t'.join(session_vars))
        if request.method == 'POST': log(f'POST: {request.POST}')
        if request.method == 'GET': log(f'GET: {request.GET}')
        if request.path != '/settings/' and 'ucs' in request.session:
            del request.session['ucs']
        if request.path[:7] != '/order/' and 'bcont' in request.session:
            del request.session['bcont']
        return func(request)
    return wrapper


def populate():
    from random import randint
    from .models import Category, User
    u = User.objects.create_user('ivan@i.ua', 'ivan', 'ivan')
    u.first_name = 'Иван'
    u.last_name = 'Иванов'
    u.phone_number = '+380997765585'
    u.address = 'Ул. Котошова, 15'
    u.save()
    for i in range(4):
        Category.objects.create(
            id=i + 1,
            name=('Телефоны', 'Ноутбуки', 'Аксессуары', 'Детали')[i])
    for i in range(10):
        Product.objects.create(
            id=i + 1,
            name='Товар ' + str(i + 1),
            description='Это описание товара №' + str(i + 1) + '.',
            category=Category.objects.get(pk=randint(1, 4)),
            amount=100 - i * randint(3, 5),
            price=(i + 1) ** 2 * 1000 - 1000 * i)
