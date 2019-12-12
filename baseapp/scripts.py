from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms import model_to_dict

from .models import Product, SingleOrder
from store.data import HtmlPages, getLogger

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

log = lambda *info: getLogger().info(' '.join(info))


def search(line='', cats=[], sort_attr='name'):
    response = Product.objects.filter(name__icontains=line)
    if cats: response = response.filter(category_id__in=[i.id for i in cats])
    response = response.order_by(sort_attr)
    return response


def auth(request, form, page):  # Main auth func for both auth and reg
    if form.is_valid():
        if page == HtmlPages.reg:
            from django.contrib.sites.shortcuts import get_current_site
            from django.utils.encoding import force_bytes
            from django.utils.http import urlsafe_base64_encode
            from django.core.mail import EmailMessage
            user = form.save()  # Saving new user
            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token.make_token(user)
            activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
    logout(request)
    return render(request, f'{page}.html', {'form': form})


def add_order(request, product_id, amount):
    product = Product.objects.get(id=product_id)
    orders = request.session.get('bcont', [])
    order_exists = False
    for item in orders:
        if item['product'] == product.id:
            order_exists = True
            item['amount'] += amount
            item['sum_price'] += float(amount*product.price)
            break
    if not order_exists:
        order = model_to_dict(SingleOrder(product=product, amount=amount, sum_price=amount*product.price))
        order.update({'sum_price': float(amount*product.price)})
        orders.append(order)
    request.session['bcont'] = orders


def populate():
    from random import randint
    from .models import Category, User
    u = User.objects.create_user('ivan@i.ua', 'ivan', 'ivan')
    u.first_name = 'Иван'
    u.last_name = 'Иванов'
    u.phone_number = '+380997765585'
    u.address = 'Ул. Котошова, 15'
    u.save()
    for i in range(4):
        Category.objects.create(
            id=i + 1,
            name=('Телефоны', 'Ноутбуки', 'Аксессуары', 'Детали')[i])
    for i in range(10):
        Product.objects.create(
            id=i + 1,
            name='Товар ' + str(i + 1),
            description='Это описание товара №' + str(i + 1) + '.',
            category=Category.objects.get(pk=randint(1, 4)),
            amount=100 - i * randint(3, 5),
            price=(i + 1) ** 2 * 1000 - 1000 * i)


def session_clear(func):
    def wrapper(request, *args):
        session_vars = [f'{k}:{v}' for k, v in request.session.items() if len(k) < 6]
        if session_vars: log("session:", ',\t'.join(session_vars))
        if request.method == 'POST': log(f'POST: {request.POST}')
        if request.path != '/settings/' and 'ucs' in request.session:
            del request.session['ucs']
        return func(request)
    return wrapper


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

token = TokenGenerator()