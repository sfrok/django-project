from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone

from store.data import SELL_STATES, STATUSES


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        # Creates and saves a User with the given params.
        if not email: raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        # Creates and saves a superuser with the given params.
        user = self.create_user(email, password=password, username=username)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def has_perm(self, perm, obj=None):  # Does the user have a specific permission?
        return True  # Simplest possible answer: Yes, always

    def has_module_perms(self, app_label):  # Does the user have permissions to view the app_label?
        return True  # Simplest possible answer: Yes, always

    @property
    def is_staff(self):  # Is the user a member of staff?
        return self.is_admin  # Simplest possible answer: All admins are staff


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=3000, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    discount = models.FloatField(default=0.0)
    amount = models.IntegerField(default=0)
    sell_state = models.IntegerField(default=0, choices=SELL_STATES)
    photo = models.ImageField(default=None)
    post_date = models.DateTimeField(default=timezone.now)
    sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price0'),
            models.CheckConstraint(check=models.Q(discount__gte=0), name='discount0'),
            models.CheckConstraint(check=models.Q(discount__lte=100), name='discount1'),
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount0'),
        ]


class Basket(models.Model):
    status = models.IntegerField(default=0, choices=STATUSES)
    date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True)
    sum_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fio = models.CharField(max_length=130, default='')
    email = models.EmailField(default='', max_length=255)
    address = models.CharField(max_length=128, default='')
    phone_number = models.CharField(max_length=16, default='')
    info = models.TextField(max_length=512, default='')

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price2')
        ]

    def __str__(self):
        return self.sum_price


class SingleOrder(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    sum_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=1), name='amount1'),
            models.CheckConstraint(check=models.Q(sum_price__gte=0), name='sum_price1')
        ]

    def __str__(self):
        return self.product.name + ' x' + str(self.amount)


class PersonalDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    expires = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=64, default='')
    value = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name
