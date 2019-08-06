from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name',
                  'username',
                  'last_name',
                  'email',
                  'password',
                  'confirm_password']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Your passwords should be equal')
