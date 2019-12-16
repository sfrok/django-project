from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import Product, User, PersonalDiscount, SingleOrder, Basket, Category

admin.site.register(Category)
admin.site.register(Product)
admin.site.unregister(Group)


class BasketInline(admin.TabularInline):
    model = Basket
    verbose_name = 'Orders'
    fields = ('id', 'date', 'status', 'sum_price', 'delivery_date',)
    readonly_fields = ('id', 'date', 'sum_price',)
    can_delete = False


class DicountInline(admin.TabularInline):
    model = PersonalDiscount
    verbose_name = 'Personal discounts'
    fields = ('name', 'value', 'expires',)
    can_delete = True


class OrderItemInline(admin.TabularInline):
    model = SingleOrder
    verbose_name = 'Items'
    fields = ('product', 'amount', 'sum_price',)
    readonly_fields = ('product', 'amount', 'sum_price',)
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    inlines = [
        BasketInline,
        DicountInline,
    ]
    readonly_fields = ('email', 'name', 'phone_number', 'address',)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password', 'password2', 'address', 'phone_number',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    verbose_name = 'Orders'
    fields = ('date', 'status', 'sum_price', 'delivery_date',)
    readonly_fields = ('date', 'status', 'sum_price', 'delivery_date',)
    inlines = [
        OrderItemInline,
    ]
