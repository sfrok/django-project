import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .auth import HtmlPages, auth, deAuth, activate, reset, change
from .forms import *
from .models import Product, Basket, Category
from .scripts import search, add_order, session_clear

f = lambda s: f'{s}.html'  # Конвертация пути в название файла: home -> home.html
check = lambda keys, post: all((key in post for key in keys))  # Ф-ия для проверки полноты POST


# AUTH

@session_clear
def reg_view(request):
    return auth(request, UserCreationForm(request.POST or None), HtmlPages.reg)


@session_clear
def auth_view(request):
    return auth(request, UserAuthorizationForm(request.POST or None), HtmlPages.auth)


@session_clear
def logout_view(request):
    return deAuth(request)


@session_clear
def home_view(request):
    greet = request.GET.get('r', False)
    return render(request, f(HtmlPages.home), {'cats': Category.objects.all(), 'greet': greet})


@session_clear
def activation_view(request):
    return activate(request, request.GET.get('uid', None), request.GET.get('token', None))


# SEARCH

@session_clear
def search_view(request):  # Страница поиска/каталога
    cat_id = request.GET.get('id', None)
    if request.method == 'POST':
        line = request.POST.get('line', '')
        sort = request.POST.get('sort', 'sold')
        if not cat_id: cat_id = request.POST.get('cat', None)
        cat = Category.objects.get(pk=cat_id) if cat_id else None
        context = {'items': search(cat, line, sort), 'sort': sort, 'cat': cat}
        return render(request, f(HtmlPages.src), context)
    cat = Category.objects.get(pk=cat_id) if cat_id else None
    return render(request, f(HtmlPages.src), {'items': search(cat), 'sort': 'sold', 'cat': cat})


# PRODUCT

@session_clear
def product_view(request):  # Страница товара
    prd_id = request.GET.get('id', None)
    if prd_id:
        product = Product.objects.get(id=prd_id)
        return render(request, f(HtmlPages.prd), {'product': product})
    return HttpResponseRedirect('/')


@session_clear
def order_add_view(request):  # Добавление товара в корзину
    if request.method == 'POST' and check(('product_count', 'pid', 'action'), request.POST):
        add_order(request)
        if request.POST['action'] == 'order':
            return HttpResponseRedirect(f'/{HtmlPages.ord}/')
        else:
            return HttpResponseRedirect(f'/{HtmlPages.prd}/?id=' + str(request.POST['pid']))
    return HttpResponseRedirect('/')


@session_clear
def order_del_view(request):  # Удаление товара из корзины
    if request.method == 'POST' and 'oid' in request.POST:
        orders = request.session.get('bcont', [])
        if orders:  # Поиск и удаление товара в корзине, если она не пустая
            for i in range(len(orders)):
                if str(orders[i]['id']) == str(request.POST['oid']):
                    del orders[i]
                    break
        if orders:
            request.session['bcont'] = orders  # Сохранение, если корзина не пустая
        elif 'bcont' in request.session:
            del request.session['bcont']  # Удаление, если пустая
        return HttpResponseRedirect(f'/{HtmlPages.ord}/')
    return HttpResponseRedirect('/')


@session_clear
def order_view(request):
    if 'bcont' in request.session:
        if 'buinfo' in request.session:
            form = OrderForm(request.session['buinfo'])
        else:
            form = OrderForm(instance=request.user if request.user.is_authenticated else None)
        c = request.session['bcont']
        return render(request, f(HtmlPages.ord), {
            'sum_price': sum((i['sum_price'] for i in c)),
            'items': [{
                'id': i['id'],
                'name': Product.objects.get(pk=i['product']).name,
                'price': i['sum_price'],
                'amount': i['amount'],
            } for i in c],
            'form': form})
    return render(request, f(HtmlPages.ord))


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bcont' in request.session:
        form = OrderForm(request.POST)
        request.session['buinfo'] = form.data
        if form.is_valid():
            # Создание объекта корзины на основе сессионной переменной
            orders = request.session['bcont']
            basket = Basket.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                sum_price=sum([i['sum_price'] for i in orders]),
                user=request.user if request.user.is_authenticated else None)
            for item in orders:  # Обработка каждого товара в корзине
                p = Product.objects.get(id=item.pop('product', None))
                item.pop('id', None)
                order = basket.singleorder_set.create(product=p, **item)
                if order.product.amount < order.amount:  # Заказ превысил кол-во товара на складе
                    basket.delete()  # Вся корзина удаляется (но не из сессии)
                    orders.remove(item)  # Конфликтный заказ убирается
                    return HttpResponseRedirect(f'/{HtmlPages.ord}/')
                # Изменение значений продаж и кол-ва товара на складе
                order.product.sold += order.amount
                order.product.amount -= order.amount
                order.product.save()
                order.save()
            del request.session['bcont']
            return render(request, f(HtmlPages.ord_com),
                          {'items': basket.singleorder_set.all(), 'order': basket})
        return HttpResponseRedirect(f'/{HtmlPages.ord}/')
    return HttpResponseRedirect('/')


# ЛИЧНЫЙ КАБИНЕТ

@session_clear
@login_required(login_url=f'/{HtmlPages.auth}/')
def cabinet_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid(): form.save()
    form = SettingsForm(instance=request.user)
    orders = Basket.objects.filter(user_id=request.user.id)
    return render(request, f(HtmlPages.cab), {'form': form, 'orders': orders})


@session_clear
def password_reset_view(request):
    success = False  # GET - поле для ввода почты
    form = UserPasswordResetForm(request.POST or None)
    if form.is_valid():  # POST - пользователь ввел почту
        reset(request, form.cleaned_data.get("email"))
        success = True  # Сообщение было отправлено
    return render(request, f(HtmlPages.reset), {'success': success, 'form': form})


@session_clear
def password_change_view(request, uidb64=None, token=None):  # for changing and resetting
    success = False  # GET - поле для ввода нового пароля
    uidb64 = request.GET.get('uid', None)
    token = request.GET.get('token', None)
    form = UserPasswordChangeForm(request.POST or None)
    if form.is_valid():  # POST - пользователь ввел новый пароль
        if not uidb64: uidb64 = request.POST.get('uidb64', None)
        if not token: token = request.POST.get('token', None)
        if not uidb64 or not token: return HttpResponseRedirect('/')
        change(request, uidb64, token, form)
        success = True  # Пароль был изменен
    if not uidb64 and not token and not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, f(HtmlPages.cng), 
        {'success': success, 'form': form, 'uidb64': uidb64, 'token': token})


# ДРУГОЕ

@session_clear
def contacts_view(request):
    return render(request, f(HtmlPages.contacts))


def not_found(request, exception=None):
    return HttpResponseRedirect('/')
