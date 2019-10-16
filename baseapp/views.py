from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserCreationForm, UserAuthorizationForm, SearchForm
from django.contrib.auth import authenticate
from .search import search
from store.data import CATEGORIES, HtmlPages
from .models import Product, User
import logging

logger = logging.getLogger('Views')


def contacts_view(request):
    return render(request, f'{HtmlPages.contacts}.html')


def registration_view(request):
    logger.info("Go to the registration page")
    reg_form = UserCreationForm(request.POST or None)
    if reg_form.is_valid():
        new_user = reg_form.save(commit=False)
        new_user.save()
        return HttpResponseRedirect(reverse('base'))
    context = {
        'reg_form': reg_form
    }
    return render(request, f'{HtmlPages.reg}.html', context)


def authorization_view(request):
    logger.info("Go to the login page")
    auth_form = UserAuthorizationForm(request.POST or None)
    if auth_form.is_valid():
        username = auth_form.cleaned_data.get("username")
        password = auth_form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            request.session['usr'] = user.id
            return HttpResponseRedirect(reverse(HtmlPages.search_input))
    context = {
        'auth_form': auth_form
    }
    return render(request, f'{HtmlPages.auth}.html', context)


# SEARCH

def search_input_view(request):
    cat = (i for i in CATEGORIES if i[0] != 'none')
    return render(request, f'{HtmlPages.search_input}.html', {'response': cat})


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

def product_view(request, _=None):
    product_id = int(request.path[9:])
    user_info = {
        'name': '',
        'address': '',
        'phone': '',
    }
    user_id = request.session.get('usr', None)
    if user_id is not None:
        user = User.get(pk=user_id)
        user_info = {
            'name': user.last_name + ' ' + user.first_name,
            'address': user.address,
            'phone': user.phone,
        }
    return render(request, f'{HtmlPages.product_page}.html',
        {'product': Product.objects.get(id=product_id), 'prefill': user_info})
