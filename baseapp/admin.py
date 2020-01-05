from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import Product, User, SingleOrder, Basket, Category

admin.site.register(Category)
admin.site.unregister(Group)


class BasketInline(admin.TabularInline):
    model = Basket
    verbose_name = 'Заказ'
    fields = ('id', 'date', 'status', 'sum_price', 'delivery_date', 
        'name', 'address', 'phone_number', 'email',)
    readonly_fields = ('id', 'date', 'sum_price', 'name', 'address', 'phone_number', 'email',)
    can_delete = True
    max_num = 0
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = SingleOrder
    verbose_name = 'Товар'
    fields = ('product', 'amount', 'sum_price',)
    readonly_fields = ('product', 'amount', 'sum_price',)
    can_delete = False
    max_num = 0
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff','is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active', 'date_joined',)}),
        ('Персональная информация', {'fields': ('name', 'phone_number', 'address',)}),
        ('Доступ', {'fields': ('is_staff',)}),
    )
    inlines = [
        BasketInline,
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
    ordering = ('date_joined', 'email',)
    filter_horizontal = ()
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    fields = ('id', 'date', 'status', 'sum_price', 'delivery_date', 
        'name', 'address', 'phone_number', 'email', 'info',)
    readonly_fields = ('id', 'date', 'sum_price', 'name', 'address', 'phone_number', 'email',)
    inlines = [
        OrderItemInline,
    ]
    list_display = ('id', 'date', 'status', 'name', 'delivery_date',)
    list_filter = ('status', 'date', 'delivery_date',)
    search_fields = ('id', 'name', 'address', 'phone_number', 'email',)
    ordering = ('date', 'id',)
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'name', 'amount', 'description', 'category', 'price', 
        'discount', 'photo',)}),
        ('Статистика', {'fields': ('post_date', 'sold',)}),
    )
    readonly_fields = ('id', 'post_date', 'sold',)
    list_display = ('id', 'name', 'amount', 'post_date', 'sold',)
    list_filter = ('category',)
    search_fields = ('id', 'name', 'amount',)
    ordering = ('id',)
