from django.contrib import admin
from django.contrib.auth.models import Group

from .forms import UserAdmin
from .models import Product, User, PersonalDiscount, SingleOrder, Basket

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(SingleOrder)
admin.site.register(PersonalDiscount)
admin.site.unregister(Group)
