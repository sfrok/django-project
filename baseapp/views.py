from django.http import HttpResponseRedirect
from django.shortcuts import render
from store.data import getLogger

from .models import Product, Basket, Category
from baseapp.scripts import HtmlPages, search, auth, add_order, populate, session_clear
from baseapp import forms
from baseapp.views_admin import *

log = lambda *info: getLogger().info(' '.join(info))


# AUTH

@session_clear
def reg_view(request):
    return auth(request, forms.UserCreationForm(request.POST or None), HtmlPages.reg)


@session_clear
def auth_view(request):
    return auth(request, forms.UserAuthorizationForm(request.POST or None), HtmlPages.auth)


@session_clear
def home_view(request):
    return render(request, f'{HtmlPages.home}.html', {'items': Category.objects.all()})


# SEARCH

@session_clear
def search_input_view(request):
    return render(request, f'{HtmlPages.srch_inp}.html', {'items': Category.objects.all()})


@session_clear
def search_result_view(request):
    if request.method == 'POST':
        line = request.POST['line']
        cats = [i for i in Category.objects.all() if request.POST['cat_' + str(i.id)]]
        return render(request, f'{HtmlPages.srch_res}.html', {'items': search(line, cats)})
    return render(request, f'{HtmlPages.srch_res}.html', {'items': search()})


# PRODUCT

@session_clear
def product_view(request):
    request.session['pid'] = int(request.path[9:])
    product = Product.objects.get(id=request.session['pid'])
    return render(request, f'{HtmlPages.product}.html', {'product': product})


@session_clear
def order_view(request):
    if request.method == 'POST':  # Добавление нового заказа в корзину
        amount = request.POST['product_count']
        add_order(request, request.session.get('pid', None), amount)
        del request.session['pid']
    if 'bcont' in request.session:
        form = forms.OrderForm(instance=request.user if request.user.is_authenticated else None)
        c = request.session.get('bcont', [])
        return render(request, f'{HtmlPages.ord}.html', {
            'sum_price': sum([i['sum_price'] for i in c]), 'items': [{
                'name': Product.objects.get(pk=i['product']).name,
                'price': i['sum_price']} for i in c], 'form': form})
    return HttpResponseRedirect('/')


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bcont' in request.session:
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            log('form data:', str(form.cleaned_data))
            # Создание корзины, если ее еще нет, или обновление уже существующей
            basket = Basket.objects.create(
                fio=form.cleaned_data['fio'],
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
                order.save()
            del request.session['bcont']
            return render(request, f'{HtmlPages.ord_com}.html')
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
        return render(request, f'{HtmlPages.settings}.html', {'form': form})
    return HttpResponseRedirect('/')


@session_clear
def order_list_view(request):
    if request.user.is_authenticated:
        orders = Basket.objects.filter(user_id=request.user.id)
        return render(request, f'{HtmlPages.ord_list}.html', {'orders': orders})
    return HttpResponseRedirect('/')


@session_clear
def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')
