from django.contrib import admin
from .models import Product, Category, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User, UserAdmin)

