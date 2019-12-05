from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Basket, Category, Product
from store.data import getLogger, SELL_STATES

log = lambda *info: getLogger().info(' '.join(info))


class UserAuthorizationForm(forms.ModelForm):
    password = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        user_in_database = User(email=self.cleaned_data.get('email'))
        if user_in_database is None:  # if current_username is empty:
            raise forms.ValidationError('Incorrect login! Try again')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2', 'address', 'phone_number',)
        labels = {'name': 'ФИО:', 'email': 'E-mail:', 'address': 'Адрес:', 'phone_number': 'Телефон:',}

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
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


class OrderForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ('name', 'email', 'address', 'phone_number')
        labels = {
            'name': 'ФИО:', 'email': 'E-mail:', 'address': 'Адрес:',
            'phone_number': 'Номер телефона:'
        }
        widgets = {i: forms.TextInput(attrs={'class':'input-field form-control'}) for i in fields}


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'address', 'phone_number')
        labels = {
            'name': 'ФИО:', 'address': 'Адрес:',
            'phone_number': 'Номер телефона:'
        }
        widgets = {i: forms.TextInput(attrs={'class':'form-control mb-2'}) for i in fields}
