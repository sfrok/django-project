from django.http import HttpResponseRedirect
from django.shortcuts import render
from store.data import getLogger

from .models import Product, Basket, Category
from baseapp.scripts import HtmlPages, search, auth, add_order, populate, session_clear
from baseapp import forms

log = lambda *info: getLogger().info(' '.join(info))
pages = [HtmlPages.auth, HtmlPages.reg, HtmlPages.settings, HtmlPages.out, HtmlPages.src]
f = lambda s: f'{s}.html'


# AUTH

@session_clear
def reg_view(request):
    return auth(request, forms.UserCreationForm(request.POST or None), HtmlPages.reg)


@session_clear
def auth_view(request):
    return auth(request, forms.UserAuthorizationForm(request.POST or None), HtmlPages.auth)


@session_clear
def home_view(request):
    return render(request, f(HtmlPages.home), {'cats': Category.objects.all(), 'pages': pages})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/')


# SEARCH

@session_clear
def search_view(request):
    if request.method == 'POST':
        log(str(request.POST))
        line = request.POST.get('line', '')
        sort = request.POST.get('sort', 'sold')
        cats = [i for i in Category.objects.all() if request.POST.get('cat_' + str(i.id), False)]
        return render(request, f(HtmlPages.src), 
            {'items': search(line, cats, sort), 'line': line, 'pages': pages, 'sort': sort})
    return render(request, f(HtmlPages.src), 
        {'items': search(sort_attr='sold'), 'line': '', 'pages': pages, 'sort': 'sold'})


# PRODUCT

@session_clear
def product_view(request):
    product = Product.objects.get(id=int(request.path[9:]))
    return render(request, f(HtmlPages.product), {'product': product, 'pages': pages})


def order_add_view(request):  # Добавление нового заказа в корзину
    log(str(request.POST))
    if request.method == 'POST' and 'product_count' in request.POST and 'pid' in request.POST:
        amount = int(request.POST['product_count'])
        add_order(request, int(request.POST['pid']), amount)
        action = request.POST.get('action', None)
        if action == 'continue': 
            return HttpResponseRedirect(f'/{HtmlPages.product}/' + str(request.POST['pid']))
        if action == 'order': return HttpResponseRedirect(f'/{HtmlPages.ord}/')
    return HttpResponseRedirect('/')


def order_del_view(request):  # Удаление заказа из корзины
    if request.method == 'POST' and 'oid' in request.POST:
        orders = request.session.get('bcont', [])
        item = 0
        for i in range(len(orders)):
            if str(orders[i]['id']) == str(request.POST['oid']):
                item = i
                break
        del orders[item]
        if orders != []: request.session['bcont'] = orders
        elif 'bcont' in request.session: del request.session['bcont']
        return HttpResponseRedirect(f'/{HtmlPages.ord}/')
    return HttpResponseRedirect('/')


@session_clear
def order_view(request):
    if 'bcont' in request.session:
        form = forms.OrderForm(instance=request.user if request.user.is_authenticated else None)
        c = request.session.get('bcont', [])
        return render(request, f(HtmlPages.ord), {
            'sum_price': sum([i['sum_price'] for i in c]), 'items': [{
                'id': i['id'], 'name': Product.objects.get(pk=i['product']).name,
                'price': i['sum_price'], 'amount': i['amount']} for i in c], 'form': form, 'pages': pages})
    return render(request, f(HtmlPages.ord), {'pages': pages})


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bcont' in request.session:
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            log('form data:', str(form.cleaned_data))
            # Создание корзины, если ее еще нет, или обновление уже существующей
            basket = Basket.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                sum_price=sum([i['sum_price'] for i in request.session.get('bcont', [])]),
                user=request.user if request.user.is_authenticated else None)
            for item in request.session.get('bcont', []):
                p = Product.objects.get(id=item.pop('product', None))
                item.update({'amount': int(item['amount'])})
                order = basket.singleorder_set.create(product=p, **item)
                if order.product.amount < order.amount:  # Заказ превысил кол-во товара на складе
                    basket.delete()  # Вся корзина удаляется (но не из сессии)
                    request.session.get('bcont', []).remove(item)  # Конфликтный заказ убирается
                    return HttpResponseRedirect(f'/{HtmlPages.ord}/')
                order.product.sold += order.amount
                order.product.amount -= order.amount
                order.product.save()
                order.save()
            del request.session['bcont']
            return render(request, f(HtmlPages.ord_com), 
                {'pages': pages, 'items': basket.singleorder_set.all(), 'order': basket})
    return HttpResponseRedirect('/')


@session_clear
def settings_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.SettingsForm(request.POST)
            if form.is_valid():
                log('form data:', str(form.cleaned_data))
                request.user.name = form.cleaned_data.get('name')
                request.user.address = form.cleaned_data.get('address')
                request.user.phone_number = form.cleaned_data.get('phone_number')
                request.user.save()
        form = forms.SettingsForm(instance=request.user)
        return render(request, f(HtmlPages.settings), {'form': form, 'pages': pages})
    return HttpResponseRedirect('/')


@session_clear
def order_list_view(request):
    if request.user.is_authenticated:
        orders = Basket.objects.filter(user_id=request.user.id)
        return render(request, f(HtmlPages.ord_list), {'orders': orders, 'pages': pages})
    return HttpResponseRedirect('/')


@session_clear
def contacts_view(request):
    return render(request, f(HtmlPages.contacts), {'pages': pages})