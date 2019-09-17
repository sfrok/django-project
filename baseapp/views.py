from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserCreationForm, UserAuthorizationForm
from django.contrib.auth import authenticate
from .search import search
import logging
logger = logging.getLogger('Views')


def contacts(request):
    return render(request, 'contacts.html')


def home(request):
    return render(request, 'base.html', {})


def registration_form(request):
    logger.info("Go to the regestration page")
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
    return render(request, "search_result.html",
                  context={'response': search('')})
