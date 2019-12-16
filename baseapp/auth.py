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
            if page == HtmlPages.reg:
                user = form.save()  # Сохранение нового пользователя
                try:  # Send an email to the user with the token:
                    user.send_mail(user.email, 'Use %s to confirm email' % user.confirmation_key)
                    # mail_subject = 'Activate your account.'
                    # current_site = get_current_site(request)
                    # uid = urlsafe_base64_encode(force_bytes(user.pk))
                    # token = tokenGen.make_token(user)
                    # activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
                    # message = "Hello {0},\n {1}".format(user.name, activation_link)
                    # to_email = form.cleaned_data.get('email')
                    # email = EmailMessage(mail_subject, message, to=[to_email])
                    # email.send()
                except: pass
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
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
    request.user.confirm_email(request.user.confirmation_key)
    request.user.is_active = True  # activate user
    request.user.save()
    return HttpResponseRedirect('/')
