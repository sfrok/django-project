from django.contrib import admin
from .models import Product, Category


admin.register([Product, Category])