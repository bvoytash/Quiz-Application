from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')


# class SignInForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
#                                                            'style': 'font-size: medium; border: solid; border-color:green; border-radius: 10px; width 30px; height: 36px',
#                                                            'placeholder': 'електронна поща',
#                                                            }))
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autofocus': True,
#                                           'style': 'font-size: medium; border: solid; border-color:green; border-radius: 10px; width 30px; height: 36px',
#                                           'placeholder': 'парола',
#                                           }))

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
