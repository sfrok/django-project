from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserCreationForm, UserAuthorizationForm, SearchForm, ProductForm
from django.contrib.auth import authenticate
from .search import search
from store.data import CATEGORIES
from .models import Product
import logging

logger = logging.getLogger('Views')


def contacts(request):
    return render(request, 'contacts.html')


def home(request):
    return render(request, 'base.html', {'response': CATEGORIES})


def registration_form(request):
    logger.info("Go to the registration page")
    reg_form = UserCreationForm(request.POST or None)
    if reg_form.is_valid():
        new_user = reg_form.save(commit=False)
        new_user.save()
        return HttpResponseRedirect(reverse('base'))
    context = {
        'reg_form': reg_form
    }
    return render(request, 'registaration.html', context)


def authorization_form(request):
    logger.info("Go to the login page")
    auth_form = UserAuthorizationForm(request.POST or None)
    if auth_form.is_valid():
        username = auth_form.cleaned_data.get("username")
        password = auth_form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return HttpResponseRedirect(reverse('home'))
    context = {
        'auth_form': auth_form
    }
    return render(request, 'auth.html', context)


def search_result(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            line = form.cleaned_data['line']
            # for i in CATEGORIES: print(form.cleaned_data[i[0]]) #############################################
            cats = [i[0] for i in CATEGORIES if form.cleaned_data[i[0]] == True]
            return render(request, "search_result.html",
                          context={'response': search(line, cat=cats)})

    # if a GET (or any other method) we'll create a blank form
    return render(request, "search_result.html",
                  context={'response': search('')})


def product(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProductForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            product_id = form.cleaned_data['id']
            return render(request, "search_result.html",
                          context={'response': Product.objects.get(id=product_id)})

    # if a GET (or any other method) we'll create a blank form
    return render(request, "search_result.html",
                  context={})
