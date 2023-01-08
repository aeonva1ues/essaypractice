from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
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
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if Profile.objects.filter(email=email).count() > 0:
            raise ValidationError('Аккаунт с такой почтой уже существует!')
        if Profile.objects.filter(username=username).count() > 0:
            raise ValidationError('Аккаунт с таким логином уже существует!')
        if ('password1' in self.cleaned_data and
                'password2' in self.cleaned_data and
                self.cleaned_data['password1'] != self.cleaned_data[
                    'password2']):
            raise ValidationError(
                'Пароли не совпали!'
            )
        return self.cleaned_data


class ChangeProfileInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('username',)
        labels = {
            'username': 'Логин'
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }
