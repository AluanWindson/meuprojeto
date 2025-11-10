from django.urls import path
from .views import (
    index,
    lista_espera,
    adicionar_pessoa,
    editar_pessoa,
    deletar_pessoa,
    pratos_view,
    login_view,
    logout_view,
    quemsomos_view,  # ✅ página "Quem Somos"
    painel_admin,    # ✅ painel administrativo real (login do Django)
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('lista/', lista_espera, name='lista_espera'),
    path('painel-admin/', painel_admin, name='painel_admin'),  # ✅ nova rota protegida por login real
    path('adicionar/', adicionar_pessoa, name='adicionar_pessoa'),
    path('editar/<int:pessoa_id>/', editar_pessoa, name='editar'),
    path('delete/<int:pessoa_id>/', deletar_pessoa, name='delete'),
    path('pratos/', pratos_view, name='pratos'),
    path('quem-somos/', quemsomos_view, name='quemsomos'),  # ✅ rota para "Quem Somos"
]
