from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Basket
from store.data import getLogger
from django.forms import Field
from django.utils.translation import gettext as _

Field.default_error_messages = {  # Локализация ошибок полей
    'required': _("Это поле обязательное."),
    'invalid': _("Пожалуйста, введите корректную информацию."),
    'max_length': _("Введенный текст слишком длинный."),
    'min_length': _("Введенный текст слишком короткий."),
    'invalid_choice': _("Пожалуйста, выберите существующую опцию."),
    'max_value': _("Введенное значение слишком велико."),
    'min_value': _("Введенное значение слишком мало."),
}


def log(*info): getLogger().info(' '.join(info))  # Ф-ия логирования


class UserAuthorizationForm(forms.ModelForm):  # Форма для авторизации пользователей
    password = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        log('UserAuthorizationForm cleaned data:', str(self.cleaned_data))
        user_in_database = User(email=self.cleaned_data.get('email'))
        if user_in_database is None:  # if current_username is empty:
            raise forms.ValidationError('Incorrect login! Try again')


class UserCreationForm(forms.ModelForm):  # Форма для создания (регистрации) пользователей

    password = forms.CharField(label='Придумайте пароль:', 
        widget=forms.PasswordInput(attrs={'class': 'input-field form-control'}))
    password2 = forms.CharField(label='Повторите пароль:', 
        widget=forms.PasswordInput(attrs={'class': 'input-field form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2', 'address', 'phone_number',)
        labels = {'name': 'ФИО:', 'email': 'E-mail:', 
            'address': 'Адрес:', 'phone_number': 'Телефон:', }
        widgets = {i: forms.TextInput(attrs={'class': 'input-field form-control'}) for i in fields}

    def clean_password2(self):  # Проверка на совпадение паролей
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error(field='password2', 
                error=forms.ValidationError(_("Пароли не совпадают!"), code='invalid'))
        return password2

    def save(self):  # Сохранение пароля в хешированном формате
        log('UserCreationForm cleaned data:', str(self.cleaned_data))
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class UserChangeForm(forms.ModelForm):  # Форма для обновления пользователей
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
        widgets = {i: forms.TextInput(attrs={'class': 'input-field form-control'}) for i in fields}


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'address', 'phone_number')
        labels = {'name': 'ФИО:', 'address': 'Адрес:', 'phone_number': 'Номер телефона:'}
        widgets = {i: forms.TextInput(attrs={'class': 'form-control mb-2'}) for i in fields}
