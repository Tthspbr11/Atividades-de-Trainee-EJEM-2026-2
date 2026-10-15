from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("produtos/adicionar/", views.adicionar_produto, name="adicionar_produto"),
    path("produtos/<int:produto_id>/remover/", views.remover_produto, name="remover_produto"),
]
