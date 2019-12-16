from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from store.data import HtmlPages

#  Для класса TokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


tokenGen = TokenGenerator()


def auth(request, form, page):  # Главная ф-ия авторизации
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            if page == HtmlPages.reg:
                user = form.save()  # Сохранение нового пользователя
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
    logout(request)
    return render(request, f'{page}.html', {'form': form})


def deAuth(request):  # Главная ф-ия деавторизации
    logout(request)
    return HttpResponseRedirect('/')


def activate(request, uidb64=None, token=None):
    request.user.is_active = True  # activate user
    request.user.save()
    return HttpResponseRedirect('/')
