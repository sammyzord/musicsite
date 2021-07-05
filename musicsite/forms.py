from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm:
    pass


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Usuário"}
        ),
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Senha"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirme a senha"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
