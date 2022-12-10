import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget

from users.models import Profile

year = datetime.date.today().year


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ('email', 'username')
        labels = {
            'email': 'Почта',
            'username': 'Логин'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if Profile.objects.filter(email=email).count() > 0:
            raise ValidationError('Аккаунт с такой почтой уже существует!')
        if Profile.objects.filter(username=username).count() > 0:
            raise ValidationError('Аккаунт с таким логином уже существует!')
        if password and password2 and password != password2:
            raise ValidationError(
                'Пароли не совпали!'
            )
        return self.cleaned_data


class ChangeProfileInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('email', 'username')
        labels = {
            'email': 'Почта',
            'username': 'Логин',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
