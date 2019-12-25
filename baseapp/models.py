from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from store.settings import EMAIL_HOST_USER

from store.data import SELL_STATES, STATUSES


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        # Creates and saves a User with the given params.
        if not email: raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # Creates and saves a superuser with the given params.
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=64, unique=True, verbose_name = "Эл. почта")
    is_active = models.BooleanField(default=False, verbose_name = "Подтвердил почту")
    is_staff = models.BooleanField(default=False, verbose_name = "Модератор")
    name = models.CharField(max_length=33, default='', verbose_name = "ФИО")
    address = models.CharField(max_length=64, default='', verbose_name = "Адрес")
    phone_number = models.CharField(max_length=16, default='', verbose_name = "Телефон")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name = "Дата регистрации")
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name

    def email_user(self, subject, message, html, from_email=EMAIL_HOST_USER, **kwargs):
        mail = EmailMultiAlternatives(subject, message, from_email, [self.email], **kwargs)
        mail.attach_alternative(html, "text/html")
        mail.send(fail_silently=True)


class Category(models.Model):
    name = models.CharField(max_length=28, default='', verbose_name = "Название")
    lore = models.TextField(max_length=3000, default='', verbose_name = "Описание")
    discount = models.FloatField(default=0.0, verbose_name = "Скидка")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        constraints = [
            models.CheckConstraint(check=models.Q(discount__gte=0), name='discount2'),
            models.CheckConstraint(check=models.Q(discount__lte=100), name='discount3'),
        ]


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name = "Название")
    description = models.TextField(max_length=3000, default='', verbose_name = "Описание")
    category = models.ForeignKey(Category, db_column='category', 
        on_delete=models.SET_NULL, null=True, verbose_name = "Категория")
    price = models.DecimalField(default=0.0, max_digits=10, 
        decimal_places=2, verbose_name = "Цена")
    discount = models.FloatField(default=0.0, verbose_name = "Скидка")
    amount = models.IntegerField(default=0, verbose_name = "Количество")
    sell_state = models.IntegerField(default=0, choices=SELL_STATES)
    photo = models.ImageField(default=None, null=True, verbose_name = "Изображение")
    post_date = models.DateTimeField(default=timezone.now, verbose_name = "Дата выставки")
    sold = models.IntegerField(default=0, verbose_name = "Продано")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price0'),
            models.CheckConstraint(check=models.Q(discount__gte=0), name='discount0'),
            models.CheckConstraint(check=models.Q(discount__lte=100), name='discount1'),
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount0'),
        ]


class Basket(models.Model):
    status = models.IntegerField(default=0, choices=STATUSES, verbose_name = "Статус")
    date = models.DateTimeField(default=timezone.now, verbose_name = "Дата оформления")
    delivery_date = models.DateTimeField(null=True, verbose_name = "Дата доставки")
    sum_price = models.DecimalField(default=0.0, max_digits=10, 
        decimal_places=2, verbose_name = "Суммарная цена")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128, default='', verbose_name = "ФИО")
    email = models.EmailField(default='', max_length=255, verbose_name = "Эл. почта")
    address = models.CharField(max_length=128, default='', verbose_name = "Адрес")
    phone_number = models.CharField(max_length=16, default='', verbose_name = "Телефон")
    info = models.TextField(max_length=512, default='', verbose_name = "Заметки модераторов")

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"
        constraints = [
            models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price2')
        ]

    def __str__(self):
        return str(self.date) + ' - ' + str(STATUSES[self.status][1]) + ' - ' + self.name


class SingleOrder(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name = "Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "Товар")
    amount = models.IntegerField(default=1, verbose_name = "Количество")
    sum_price = models.DecimalField(default=0.0, max_digits=10, 
        decimal_places=2, verbose_name = "Суммарная цена")

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=1), name='amount1'),
            models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price1')
        ]

    def __str__(self):
        return self.product.name + ' x' + str(self.amount)
