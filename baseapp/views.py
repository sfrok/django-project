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
def registration_view(request):
    return auth(request, forms.UserCreationForm(request.POST or None), HtmlPages.reg)


@session_clear
def authorization_view(request):
    return auth(request, forms.UserAuthorizationForm(request.POST or None), HtmlPages.auth)


# SEARCH

@session_clear
def search_input_view(request):
    return render(request, f'{HtmlPages.srch_inp}.html', {'items': Category.objects.all()})


@session_clear
def search_result_view(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            log('form data:', str(form.cleaned_data))
            line = form.cleaned_data['line']
            cats = [i for i in Category.objects.all() if form.cleaned_data['cat_' + str(i.id)]]
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
        form = forms.SingleOrderForm(request.POST)
        if form.is_valid() and 'pid' in request.session:
            log('form data:', str(form.cleaned_data))
            amount = form.cleaned_data['product_count']
            add_order(request, request.session.get('pid', None), amount)
            del request.session['pid']
    if 'bcont' in request.session:
        c = request.session.get('bcont', [])
        return render(request, f'{HtmlPages.ord}.html', {
            'sum_price': sum([i['sum_price'] for i in c]), 'items': [{
                'name': Product.objects.get(pk=i['product']).name,
                'price': i['sum_price']} for i in c]})
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
                    return HttpResponseRedirect('/order/')
                order.product.sold += order.amount
                order.product.amount -= order.amount
                order.save()
            del request.session['bcont']
            return render(request, f'{HtmlPages.ord_com}.html')
    return HttpResponseRedirect('/')


@session_clear
def settings_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'ucs' in request.session:
            form = forms.SettingsForm(request.POST)
            if form.is_valid():
                log('form data:', str(form.cleaned_data))
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.email = form.cleaned_data['email']
                request.user.address = form.cleaned_data['address']
                request.user.phone_number = form.cleaned_data['phone_number']
                request.user.save()
                return render(request, f'{HtmlPages.settings}.html')
        else:
            request.session['ucs'] = True
        return render(request, f'{HtmlPages.settings}.html')
    return HttpResponseRedirect('/')


@session_clear
def order_list_view(request):
    if request.user.is_authenticated:
        orders = Basket.objects.filter(user_id=request.user.id)
        return render(request, f'{HtmlPages.ord_list}.html', {'orders': orders})
    return HttpResponseRedirect('/')


@session_clear
def home_view(request):
    return render(request, f'{HtmlPages.home}.html', {'items': Category.objects.all()})


@session_clear
def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')
