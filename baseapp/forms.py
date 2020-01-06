from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate

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

    class Meta:
        _attrs = {'class': 'login-form'}
        _fields = (
            ('email', _('Введите почту:'), forms.EmailInput(_attrs)),
            ('password', _('Введите пароль:'), forms.PasswordInput(_attrs))
        )
        model = User
        fields = tuple(f[0] for f in _fields)
        labels = {f[0]: f[1] for f in _fields}
        widgets = {f[0]: f[2] for f in _fields}

    def clean(self):
        log('UserAuthorizationForm cleaned data:', str(self.cleaned_data))
        user = authenticate(email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'))
        if user is None:  # if current_username is empty:
            raise forms.ValidationError('Неправильные почта или пароль!')


class UserCreationForm(forms.ModelForm):  # Форма для создания (регистрации) пользователей
    _attrs = {'class': 'reg-form'}
    password = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput(_attrs))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(_attrs))

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password2', 'address', 'phone_number',)
        labels = {'name': 'ФИО:', 'email': 'E-mail:', 
            'address': 'Адрес:', 'phone_number': 'Телефон:', }
        widgets = {i: forms.TextInput({'class': 'reg-form'}) for i in fields}

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


class UserPasswordResetEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput({'class': 'res-form'}))


class UserPasswordResetForm(forms.ModelForm):  # Форма смены пароля
    _attrs = {'class': 'chng-form mb-1'}
    password = forms.CharField(label='Новый пароль:', widget=forms.PasswordInput(_attrs))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(_attrs))

    class Meta:
        model = User
        fields = ('password', 'password2',)

    def clean_password(self):  # Проверка на совпадение паролей
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error(field='password', 
                error=forms.ValidationError(_("Пароли не совпадают!"), code='invalid'))
        return password

    def clean_password2(self):  # Проверка на совпадение паролей
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error(field='password2', 
                error=forms.ValidationError(_("Пароли не совпадают!"), code='invalid'))
        return password2


class UserPasswordChangeForm(forms.ModelForm):
    _attrs = {'class': 'input-field form-control mb-1'}
    password_old = forms.CharField(label='Старый пароль:', widget=forms.PasswordInput(_attrs))
    password = forms.CharField(label='Новый пароль:', widget=forms.PasswordInput(_attrs))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(_attrs))
    email = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'password_old',)

    def clean_password(self):  # Проверка на совпадение паролей
        log('new', self.cleaned_data)
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error(field='password', 
                error=forms.ValidationError(_("Пароли не совпадают!"), code='invalid'))
        return password

    def clean_password2(self):  # Проверка на совпадение паролей
        log('repeat', self.cleaned_data)
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error(field='password2', 
                error=forms.ValidationError(_("Пароли не совпадают!"), code='invalid'))
        return password2

    def clean_password_old(self):  # Проверка на совпадение паролей
        log('old', self.cleaned_data)
        password = self.cleaned_data.get("password_old")
        user = authenticate(email=self.cleaned_data.get('email'), password=password)
        if user is None:  # if current_username is empty:
            self.add_error(field='password_old', 
                error=forms.ValidationError(_("Неверный пароль!"), code='invalid'))
        return password

    def clean(self):
        log('UserPasswordChangeForm cleaned data:', str(self.cleaned_data))
        super().clean()

    def save(self):  # Сохранение пароля в хешированном формате
        log('UserPasswordChangeForm save data:', str(self.cleaned_data))
        user = authenticate(email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password_old'))
        if user is None:  # if current_username is empty:
            raise forms.ValidationError('Не удалось сменить пароль!')
        else:
            user.set_password(self.cleaned_data["password"])
            user.save()
        return user


class UserChangeForm(forms.ModelForm):  # Форма для обновления пользователей
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff')

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
