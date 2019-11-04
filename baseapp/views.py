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
        print("\nrequest (path, method):", request.path, request.method)
        print(f'\t- session:', ', '.join([f'{k}:{v}' for k, v in request.session.items() if len(k) < 6]))
        if request.method == 'POST': print(f'\t- POST: {request.POST}\n')

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
    return auth(request, forms.UserCreationForm(request.POST or None), HtmlPages.reg)


@session_clear
def authorization_view(request):
    return auth(request, forms.UserAuthorizationForm(request.POST or None), HtmlPages.auth)


# SEARCH

@session_clear
def search_input_view(request):
    cats = (i for i in CATEGORIES if i[0])
    return render(request, f'{HtmlPages.search_input}.html', {'response': cats})


@session_clear
def search_result_view(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            line = form.cleaned_data['line']
            cats = [i[0] for i in CATEGORIES if i[0] and form.cleaned_data[i[0]]]
            return render(request, f'{HtmlPages.search_result}.html', {'response': search(line, cats)})
    return render(request, f'{HtmlPages.search_result}.html', {'response': search()})


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
            amount = form.cleaned_data['product_count']
            add_order(request, request.session.get('pid', None), amount)
            del request.session['pid']
    return render(request, f'{HtmlPages.ord}.html', 
        {'sum_price': sum([i['sum_price'] for i in request.session.get('bcont', [])])})


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bcont' in request.session:
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            # Создание корзины, если ее еще нет, или обновление уже существующей
            basket = Basket.objects.create(
                fio = form.cleaned_data['fio'],
                email = form.cleaned_data['email'],
                address = form.cleaned_data['address'],
                phone_number = form.cleaned_data['phone_number'],
                sum_price = sum([i['sum_price'] for i in request.session.get('bcont', [])]),
                user_id = request.user.id if request.user.is_authenticated else 0)
            for item in request.session.get('bcont', []):
                order = basket.singleorder_set.create(**item)
                order.product.sold += 1
                order.product.amount -= order.amount
                order.save()
            del request.session['bcont']
            return render(request, f'{HtmlPages.com_ord}.html')
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
    if request.user.is_authenticated:
        orders = Basket.objects.filter(user_id=request.user.id)
        return render(request, f'{HtmlPages.ord_list}.html', {'orders': orders})
    return HttpResponseRedirect('/')


@session_clear
def home_view(request):
    cats = (i for i in CATEGORIES if i[0])
    return render(request, f'{HtmlPages.home}.html', {'response': cats})


@session_clear
def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')


def add_order(request, product_id, amount):
    product = Product.objects.get(id=product_id)
    order = SingleOrder(product=product, amount=amount, sum_price=product.price)
    orders = request.session.get('bcont', [])
    orders.append(model_to_dict(order))
    request.session['bcont'] = orders
