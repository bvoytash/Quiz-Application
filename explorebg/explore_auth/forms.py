from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = UserModel
#         fields = ('email', 'password1', 'password2')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'style': 'font-size: medium; border: solid; border-color: green; border-radius: 10px; width: 100%; height: 36px',
            'placeholder': 'електронна поща',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'style': 'font-size: medium; border: solid; border-color: green; border-radius: 10px; width: 100%; height: 36px',
            'placeholder': 'парола',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'style': 'font-size: medium; border: solid; border-color: green; border-radius: 10px; width: 100%; height: 36px',
            'placeholder': 'потвърдете паролата',
        })
    )

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'style': 'font-size: medium; border: solid; border-color:green; border-radius: 10px; width 30px; height: 36px',
            'placeholder': 'електронна поща',
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True,
            'style': 'font-size: medium; border: solid; border-color:green; border-radius: 10px; width 30px; height: 36px',
            'placeholder': 'парола',
        }))
