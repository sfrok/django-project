from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationForm, UserAuthorizationForm, SearchForm, \
    OrderForm, OrderCompleteForm, SettingsForm
from django.contrib.auth import authenticate, login, logout
from .search import search
from store.data import CATEGORIES, HtmlPages
from .models import Product, User, SingleOrder, Basket
import logging

logger = logging.getLogger('Views')


def session_clear(func):
    def wrapper(request, *_):
        print("request.(path, method):", request.method, request.path)
        if request.method == 'POST': print("request.POST:", request.POST)
        if 'pid' in request.session: print('request.session.pid:', request.session['pid'])
        if 'bid' in request.session: print('request.session.bid:', request.session['bid'])

        if request.path != '/settings/' and 'ucs' in request.session:
            del request.session['ucs']
        if request.path[:9] != '/product/' and request.path != '/order/':
            if 'pid' in request.session: del request.session['pid']

        response = func(request)
        return response
    return wrapper


@session_clear
def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')


@session_clear
def registration_view(request):
    logger.info("Go to the registration page")
    reg_form = UserCreationForm(request.POST or None)
    if reg_form.is_valid():
        new_user = reg_form.save(commit=False)
        new_user.save()
        username = reg_form.cleaned_data.get("username")
        password = reg_form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
    context = {
        'reg_form': reg_form
    }
    logout(request)
    return render(request, f'{HtmlPages.reg}.html', context)


@session_clear
def authorization_view(request):
    logger.info("Go to the login page")
    auth_form = UserAuthorizationForm(request.POST or None)
    if auth_form.is_valid():
        username = auth_form.cleaned_data.get("username")
        password = auth_form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
    logout(request)
    return render(request, f'{HtmlPages.auth}.html', {'auth_form': auth_form})


# SEARCH

@session_clear
def search_input_view(request):
    cat = (i for i in CATEGORIES if i[0] != 'none')
    return render(request, f'{HtmlPages.search_input}.html', {'response': cat})


@session_clear
def search_result_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
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
    if request.method == 'POST' and 'pid' in request.session:
        form = OrderForm(request.POST)
        if form.is_valid():
            # Презаполнение формы
            user_info = {'name': '', 'phone': '', 'email': '', 'address': '', }
            if request.user.is_authenticated:
                user_info = {
                    'name': request.user.last_name + ' ' + request.user.first_name,
                    'phone': request.user.phone_number,
                    'email': request.user.email,
                    'address': request.user.address,
                }

            # Создание корзины, если ее еще нет
            basket = Basket()
            if 'bid' in request.session and 'bcont' in request.session:
                basket.__dict__.update(request.session.get('bid', None))
                if request.user.is_authenticated:
                    basket.user = request.user.id
                container = request.session.get('bcont', None)
            else:
                container = []

            # Добавление нового заказа в корзину
            product = Product.objects.get(id=request.session.get('pid', None))
            amount = form.cleaned_data['product_count']
            order = SingleOrder(basket_id=basket.id, product=product, amount=amount)
            container.append(model_to_dict(order))
            del request.session['pid']

            tmp = model_to_dict(basket)
            del tmp['date']
            del tmp['delivery_date']
            request.session['bid'] = tmp
            request.session['bcont'] = container
            return render(request, f'{HtmlPages.ord}.html',
                  {'prefill': user_info})
    return HttpResponseRedirect('/')


@session_clear
def order_complete_view(request):
    if request.method == 'POST' and 'bid' in request.session and 'bcont' in request.session:
        form = OrderCompleteForm(request.POST)
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
            form = SettingsForm(request.POST)
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
def order_list(request):
    return render(request, f'{HtmlPages.order_list}.html')


@session_clear
def home_view(request):
    cat = (i for i in CATEGORIES if i[0] != 'none')
    return render(request, f'{HtmlPages.home}.html', {'response': cat})


"""
@session_clear
def order_view(request):
        # Презаполнение формы
        user_info = {'name': '', 'address': '', 'phone': '', }
        user_id = request.session.get(usr, None)
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            user_info = {
                'name': user.last_name + ' ' + user.first_name,
                'address': user.address,
                'phone': user.phone_number,
            }

        # Создание корзины, если ее еще нет
        if 'bid' in request.session and 'bcont' in request.session:
            basket = request.session.get('bid', None)
            container = request.session.get('bcont', None)
        elif user_id is not None:
            try:
                basket = Basket.objects.get(status=0)
            except basket.DoesNotExist:
                basket = Basket(user=user_id)
            container = [i for i in SingleOrder.objects.filter(basket_id=basket.id)]
        else:
            basket = Basket()
            container = []
        if user_id is not None: basket.save()

        request.session['bid'] = basket
        request.session['bcont'] = container
        return render(request, f'{HtmlPages.ord}.html', {'prefill': user_info})
    return render(request, f'{HtmlPages.home}.html')
"""
