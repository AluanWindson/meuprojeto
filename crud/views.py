from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Pessoa, Avaliacao


def index(request):
    mensagem = ""
    senha_erro = ""

    if request.method == "POST":
        # 🔹 FORMULÁRIO DO CLIENTE (PEDIDO)
        if 'form_cliente' in request.POST:
            nome = request.POST.get('nome')
            idade = request.POST.get('idade')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            cpf = request.POST.get('cpf')
            qtd_pessoas = request.POST.get('qtd_pessoas')
            prato_selecionado = request.POST.get('prato_selecionado')  # <-- campo vindo do index.html

            if nome and idade and email and telefone and cpf and qtd_pessoas and prato_selecionado:
                Pessoa.objects.create(
                    nome=nome,
                    idade=int(idade),
                    email=email,
                    telefone=telefone,
                    cpf=cpf,
                    qtd_pessoas=int(qtd_pessoas),
                    prato_selecionado=prato_selecionado  # <-- salva corretamente no banco
                )
                mensagem = "Cadastro realizado com sucesso! Aguarde na lista de espera."
            else:
                mensagem = "Por favor, preencha todos os campos."

        # 🔹 FORMULÁRIO DE ACESSO ADMINISTRATIVO (SENHA SIMPLES)
        elif 'form_senha' in request.POST:
            senha = request.POST.get('senha')
            if senha == "12345":
                # 🔒 Redireciona apenas para a lista de pedidos e comentários
                return redirect('lista_espera')
            else:
                senha_erro = "Senha incorreta."

        # 🔹 FORMULÁRIO DE AVALIAÇÃO
        elif 'comentario' in request.POST:
            comentario_texto = request.POST.get('comentario')
            cpf_avaliacao = request.POST.get('cpf_avaliacao')
            nota = request.POST.get('nota')

            if comentario_texto and cpf_avaliacao:
                try:
                    pessoa = Pessoa.objects.get(cpf=cpf_avaliacao)
                    Avaliacao.objects.create(
                        pessoa=pessoa,
                        comentario=comentario_texto,
                        nota=int(nota) if nota else 0
                    )
                    mensagem = "Avaliação enviada com sucesso!"
                except Pessoa.DoesNotExist:
                    mensagem = "CPF não encontrado. Avaliação não adicionada."

    # 🔹 Dados para exibição
    pessoas = Pessoa.objects.all()
    avaliacoes = Avaliacao.objects.all().order_by('-criado_em')

    return render(
        request,
        "index.html",
        {
            "mensagem": mensagem,
            "senha_erro": senha_erro,
            "pessoas": pessoas,
            "avaliacoes": avaliacoes
        }
    )


# 🔒 LOGIN REAL USANDO DJANGO
def login_view(request):
    erro = ""
    if request.method == "POST":
        username = request.POST.get('login')
        senha = request.POST.get('senha')
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            # ✅ Agora redireciona para o painel geral (não para pedidos)
            return redirect('painel_admin')
        else:
            erro = "Usuário ou senha incorretos."
    return render(request, 'login.html', {'erro': erro})


def logout_view(request):
    logout(request)
    return redirect('login')


# 🔒 LISTA DE PEDIDOS E COMENTÁRIOS (acesso por senha simples)
@login_required(login_url='login')
@never_cache
def lista_espera(request):
    pessoas = Pessoa.objects.all()
    avaliacoes = Avaliacao.objects.all().order_by('-criado_em')
    contexto = {
        'pessoas': pessoas,
        'avaliacoes': avaliacoes
    }
    return render(request, 'lista_espera.html', contexto)


# 🔒 PAINEL ADMINISTRATIVO GERAL (acesso por login do Django)
@login_required(login_url='login')
@never_cache
def painel_admin(request):
    return render(request, 'painel_admin.html')


@login_required(login_url='login')
@never_cache
def adicionar_pessoa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        qtd_pessoas = request.POST.get('qtd_pessoas')
        prato_selecionado = request.POST.get('prato_selecionado')

        if nome and idade and telefone and email and cpf and qtd_pessoas and prato_selecionado:
            Pessoa.objects.create(
                nome=nome,
                idade=int(idade),
                telefone=telefone,
                email=email,
                cpf=cpf,
                qtd_pessoas=int(qtd_pessoas),
                prato_selecionado=prato_selecionado
            )
            return redirect('lista_espera')

    return render(request, 'adicionar_pessoa.html')


@login_required(login_url='login')
@never_cache
def editar_pessoa(request, pessoa_id):
    pessoa = Pessoa.objects.get(id=pessoa_id)

    if request.method == 'POST':
        pessoa.nome = request.POST.get('nome')
        pessoa.idade = int(request.POST.get('idade'))
        pessoa.telefone = request.POST.get('telefone')
        pessoa.email = request.POST.get('email')
        pessoa.cpf = request.POST.get('cpf')
        pessoa.qtd_pessoas = int(request.POST.get('qtd_pessoas'))
        pessoa.prato_selecionado = request.POST.get('prato_selecionado')
        pessoa.save()
        return redirect('lista_espera')

    return render(request, 'editar_pessoa.html', {'pessoa': pessoa})


@login_required(login_url='login')
@never_cache
def deletar_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    if request.method == 'POST':
        pessoa.delete()
        return redirect('lista_espera')
    return render(request, 'crud/confirmar_delete.html', {'pessoa': pessoa})


def pratos_view(request):
    return render(request, 'pratos.html')


def quemsomos_view(request):
    return render(request, 'quemsomos.html')
