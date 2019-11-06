from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import model_to_dict

from .models import Product, SingleOrder
from store.data import HtmlPages


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
    order = SingleOrder(product=product, amount=amount, sum_price=product.price)
    orders = request.session.get('bcont', [])
    orders.append(model_to_dict(order))
    request.session['bcont'] = orders
