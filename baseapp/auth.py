from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from store.data import HtmlPages
from django.utils.translation import gettext as _
from .models import User

#  Для класса TokenGenerator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


tokenGen = TokenGenerator()


def encodeLink(request, user, page):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = tokenGen.make_token(user)
    return '{0}/{1}/?uid={2}&token={3}'.format(current_site, page, uid, token)


def decodeLink(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


def auth(request, form, page):  # Главная ф-ия авторизации
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            if page == HtmlPages.reg:
                user = form.save()  # Сохранение нового пользователя
                subject = _('Активация аккаунта')
                link = encodeLink(request, user, HtmlPages.act)
                text = (_("Здравствуйте"), _("перейдите по этой ссылке для активации"))
                message = makeEmail(text, user.name, link)
                user.email_user(subject, message)
                return HttpResponseRedirect('/?r=')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
    logout(request)
    return render(request, f'{page}.html', {'form': form})


def activate(request, uidb64, token):
    user = decodeLink(request, uidb64)
    if user is not None and tokenGen.check_token(user, token):
        user.is_active = True  # Активация пользователя
        user.save()
        login(request, user)
    return HttpResponseRedirect('/')


def reset(request, email):  # Главная ф-ия авторизации
    user = User.objects.get(email=email)
    subject = 'Восстановление пароля'
    link = encodeLink(request, user, HtmlPages.cng)
    text = (_("Здравствуйте"), _("перейдите по этой ссылке для восстановления пароля"))
    message = makeEmail(text, user.name, link)
    user.email_user(subject, message)


def change(request, uidb64, token, form):
    user = decodeLink(request, uidb64)
    if user is not None and tokenGen.check_token(user, token):
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(request, user)

def deAuth(request):  # Главная ф-ия деавторизации
    logout(request)
    return HttpResponseRedirect('/')


def makeEmail(text, name, link):
    return """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
            <p>
            {0}, {1}, {2}:<br>
            <a href="{3}">{3}</a>
            </p>
        </body>
        </html>
        """.format(text[0], name, text[1], link)