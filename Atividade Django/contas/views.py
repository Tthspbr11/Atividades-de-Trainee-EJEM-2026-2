from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroForm, LoginForm, ProdutoForm
from .models import Produto


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect("login")
    else:
        form = CadastroForm()
    return render(request, "contas/cadastro.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    erro = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
        erro = "Nome de usuário ou senha incorretos."
    else:
        form = LoginForm()
    return render(request, "contas/login.html", {"form": form, "erro": erro})


@login_required
def home(request):
    produtos = request.user.produtos.all().order_by("nome")
    form = ProdutoForm()
    return render(request, "contas/home.html", {"produtos": produtos, "form": form})


@login_required
@require_POST
def adicionar_produto(request):
    form = ProdutoForm(request.POST)
    if form.is_valid():
        produto = form.save(commit=False)
        produto.usuario = request.user
        produto.save()
        messages.success(request, f"Produto '{produto.nome}' adicionado.")
    else:
        messages.error(request, "Informe um nome e uma quantidade válida.")
    return redirect("home")


@login_required
@require_POST
def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, usuario=request.user)
    nome = produto.nome
    produto.delete()
    messages.success(request, f"Produto '{nome}' removido.")
    return redirect("home")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")
