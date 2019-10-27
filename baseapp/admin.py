from .forms import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, User, PersonalDiscount, Order

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(PersonalDiscount)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
