import logging

from django.contrib.auth import authenticate, login, logout
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render

from baseapp import forms
from store.data import CATEGORIES, HtmlPages
from .models import Product, SingleOrder, Basket
from .search import search

logger = logging.getLogger('Views')


def session_clear(func):
    def wrapper(request, *args):
        print("request (path, method):", request.path, request.method)
        if request.method == 'POST': print("- POST:", request.POST)
        for i in ('ucs', 'pid', 'bid', 'bcont'):
            if i in request.session: print(f'- session {i}:', request.session[i])

        if request.path != '/settings/' and 'ucs' in request.session:
            del request.session['ucs']
        if request.path[:9] != '/product/' and request.path != '/order/':
            if 'pid' in request.session: del request.session['pid']
        return func(request)
    return wrapper


# AUTH

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


@session_clear
def registration_view(request):
    form = forms.UserCreationForm(request.POST or None)
    return auth(request, form, HtmlPages.reg)


@session_clear
def authorization_view(request):
    form = forms.UserAuthorizationForm(request.POST or None)
    return auth(request, form, HtmlPages.auth)


# SEARCH

@session_clear
def search_input_view(request):
    cat = (i for i in CATEGORIES if i[0] != 'none')
    return render(request, f'{HtmlPages.search_input}.html', {'response': cat})


@session_clear
def search_result_view(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            line = form.cleaned_data['line']
            cats = [i[0] for i in CATEGORIES if i[0] != 'none' and form.cleaned_data[i[0]]]
            return render(request, f'{HtmlPages.search_result}.html',
                          {'response': search(line, cat=(cats if cats != [] else None))})
    return render(request, f'{HtmlPages.search_result}.html', {'response': search('')})


# PRODUCT

@session_clear
def product_view(request, _=None):
    print(request.path[:9])
    product_id = int(request.path[9:])
    product = Product.objects.get(id=product_id)
    request.session['pid'] = product_id
    return render(request, f'{HtmlPages.product}.html', {'product': product})


@session_clear
def order_view(request):
    # Создание корзины, если ее еще нет, или обновление уже существующей
    basket = request.session.get('bid', Basket())
    container = request.session.get('bcont', [])
    if request.method == 'POST':  # Добавление нового заказа в корзину
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            if 'pid' in request.session:
                amount = form.cleaned_data['product_count']
                add_order(request, request.session.get('pid', None), amount, basket.id)
                del request.session['pid']
    if request.user.is_authenticated:
        basket.user_id = request.user.id
    basket_dict = model_to_dict(basket)
    del basket_dict['date']
    del basket_dict['delivery_date']
    request.session['bid'] = basket_dict
    request.session['bcont'] = container
    return render(request, f'{HtmlPages.ord}.html')


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bid' in request.session and 'bcont' in request.session:
        form = forms.OrderCompleteForm(request.POST)
        if form.is_valid():
            basket = Basket()
            basket.__dict__.update(request.session.get('bid', None))
            container = request.session.get('bcont', None)
            basket.fio = form.cleaned_data['fio']
            basket.save()
            for item in container:
                order = SingleOrder()
                order.__dict__.update(item)
                order.product.sold -= 1
                order.product.amount -= order.amount
                order.save()
            del request.session['bid']
            del request.session['bcont']
            return render(request, f'{HtmlPages.com_ord}.html',
                          {'basket': basket, 'orders': container})
    return HttpResponseRedirect('/')


@session_clear
def settings_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'ucs' in request.session:
            form = forms.SettingsForm(request.POST)
            if form.is_valid():
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.email = form.cleaned_data['email']
                request.user.address = form.cleaned_data['address']
                request.user.phone_number = form.cleaned_data['phone_number']
                request.user.save()
                return render(request, f'{HtmlPages.settings}.html')
        else: request.session['ucs'] = True
        return render(request, f'{HtmlPages.settings}.html')
    return HttpResponseRedirect('/')


@session_clear
def order_list_view(request):
    orders = Basket.objects.filter(user_id=request.user.id)
    return render(request, f'{HtmlPages.ord_list}.html', {'orders': orders})


@session_clear
def home_view(request):
    cat = (i for i in CATEGORIES if i[0] != 'none')
    return render(request, f'{HtmlPages.home}.html', {'response': cat})


@session_clear
def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')


def add_order(request, product_id, amount, basket_id):
    product = Product.objects.get(id=product_id)
    order = SingleOrder(basket_id=basket_id, product=product, amount=amount)
    container = request.session.get('bcont', [])
    container.append(model_to_dict(order))
    request.session['bcont'] = container
