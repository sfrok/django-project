from django.db import models
from django.utils import timezone
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)


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


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'password',
                  'confirm_password']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Your passwords should be equal')

