from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    a_country = models.CharField(max_length=128)
    a_city = models.CharField(max_length=128)
    a_address = models.CharField(max_length=128)
    post_index = models.IntegerField(default=0)
    payment_info = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=3000)
    categories = models.ManyToManyField(Category)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    discount = models.FloatField(default=0.0)
    amount = models.IntegerField(default=0)
    selling_type = models.IntegerField(default=0)
    ship_to = models.TextField(max_length=300)
    ship_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    ship_discount = models.FloatField(default=0.0)
    photo = models.ImageField()
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price0'),
            models.CheckConstraint(check=models.Q(ship_price__gte=0), name='ship_price0'),
            models.CheckConstraint(check=models.Q(discount__gte=0), name='discount0'),
            models.CheckConstraint(check=models.Q(discount__lte=100), name='discount1'),
            models.CheckConstraint(check=models.Q(ship_discount__gte=0), name='ship_discount0'),
            models.CheckConstraint(check=models.Q(ship_discount__lte=100), name='ship_discount1'),
            models.CheckConstraint(check=models.Q(amount__gte=0), name='amount0'),
        ]

class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    product = ForeignKey(Product, on_delete=models.CASCADE)
    status = ForeignKey(Status, on_delete=models.CASCADE)
    date = models.DataTimeField(default=timezone.now)
    delivery_date = models.DataTimeField(default=timezone.now)
    amount = models.IntegerField(default=1)
    sum_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    sum_ship_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(check-models.Q(amount__gte=1), name='amount1'),
            models.CheckConstraint(check-models.Q(sum_price__gte=0), name='sim_price1')
        ]


class Status(models.Model):
    name = models.CharFields(max_lenght=32)


class PersonalDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    expires = models.DateTimeField
    name = models.CharField(max_length=64)
    value = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name
