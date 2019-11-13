from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Category
from store.data import getLogger, SELL_STATES

log = lambda *info: getLogger().info(' '.join(info))


class UserAuthorizationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        current_username = self.cleaned_data.get('username')
        user_in_database = User(username=current_username)
        if user_in_database is None:  # if current_username is empty:
            raise forms.ValidationError('Incorrect login! Try again')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password', 'password2', 'address',
                  'phone_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username',
                                      'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username',
                       'email', 'password', 'password2', 'address',
                       'phone_number',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class SearchForm(forms.Form):
    line = forms.CharField(max_length=100, required=False)
    log(', '.join(['cat_' + str(i.id) for i in Category.objects.all()]))
    locals().update(
        {'cat_' + str(i.id): forms.BooleanField(required=False) for i in Category.objects.all()})


class SingleOrderForm(forms.Form):
    product_count = forms.CharField(max_length=130, required=False)


class OrderForm(forms.Form):
    fio = forms.CharField(max_length=130, required=False)
    email = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=128, required=False)
    phone_number = forms.CharField(max_length=16, required=False)


class SettingsForm(forms.Form):
    first_name = forms.CharField(max_length=64, required=False)
    last_name = forms.CharField(max_length=64, required=False)
    email = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=128, required=False)
    phone_number = forms.CharField(max_length=16, required=False)


class AdminCatForm(forms.Form):
    name = forms.CharField(max_length=32, required=False)


class AdminProductForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=3000, required=False, widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    discount = forms.FloatField(required=False)
    amount = forms.IntegerField(required=False)
    sell_state = forms.ChoiceField(choices=SELL_STATES, required=False)
    photo = forms.ImageField(required=False)
