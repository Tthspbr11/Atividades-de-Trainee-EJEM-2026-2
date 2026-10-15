from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Produto


class CadastroForm(forms.Form):
    username = forms.CharField(label="Nome de usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        cleaned = super().clean()
        senha = cleaned.get("password")
        confirmar = cleaned.get("confirmar_senha")
        if senha and confirmar and senha != confirmar:
            self.add_error("confirmar_senha", "As senhas não coincidem.")
        elif senha:
            try:
                validate_password(senha)
            except forms.ValidationError as erro:
                self.add_error("password", erro)
        return cleaned

    def save(self):
        return User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )


class LoginForm(forms.Form):
    username = forms.CharField(label="Nome de usuário", max_length=150)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "quantidade"]
        labels = {"nome": "Nome do produto", "quantidade": "Quantidade"}
        widgets = {"quantidade": forms.NumberInput(attrs={"min": 1})}
