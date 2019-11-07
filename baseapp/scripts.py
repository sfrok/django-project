from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import model_to_dict

from .models import Product, SingleOrder
from store.data import HtmlPages, getLogger

log = lambda *info: getLogger().info(' '.join(info))


def search(line='', cats=[], sort_attr='name'):
    response = Product.objects.filter(name__icontains=line)
    if cats: response = response.filter(category_id__in=[i.id for i in cats])
    response = response.order_by(sort_attr)
    return response


def auth(request, form, page):  # Main auth func for both auth and reg
    if form.is_valid():
        if page == HtmlPages.reg:
            (form.save(commit=False)).save()  # Saving new user
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
    logout(request)
    return render(request, f'{page}.html', {'login_form': form})


def add_order(request, product_id, amount):
    product = Product.objects.get(id=product_id)
    order = SingleOrder(product=product, amount=amount, sum_price=amount*product.price)
    orders = request.session.get('bcont', [])
    orders.append(model_to_dict(order))
    request.session['bcont'] = orders


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
