from django.contrib import admin
from .models import Pessoa, Avaliacao

# Inline para mostrar avaliações dentro do admin da Pessoa
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0  # não mostra linhas extras vazias
    readonly_fields = ('nota', 'comentario', 'criado_em')  # só leitura
    can_delete = False  # não permite deletar pelo inline


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'telefone', 'email', 'cpf', 'qtd_pessoas')
    fields = ('nome', 'idade', 'telefone', 'email', 'cpf', 'qtd_pessoas')
    search_fields = ('nome', 'email', 'telefone', 'cpf')
    inlines = [AvaliacaoInline]  # ✅ Exibe as avaliações diretamente dentro da página da pessoa


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('get_nome_pessoa', 'get_cpf_pessoa', 'nota', 'comentario', 'criado_em')
    list_filter = ('nota', 'criado_em')
    search_fields = ('pessoa__nome', 'pessoa__cpf', 'comentario')

    def get_nome_pessoa(self, obj):
        """Retorna o nome da pessoa associada à avaliação."""
        return obj.pessoa.nome if obj.pessoa else "(Pessoa removida)"
    get_nome_pessoa.admin_order_field = 'pessoa'
    get_nome_pessoa.short_description = 'Pessoa'

    def get_cpf_pessoa(self, obj):
        """Retorna o CPF da pessoa associada à avaliação."""
        return obj.pessoa.cpf if obj.pessoa and obj.pessoa.cpf else "—"
    get_cpf_pessoa.short_description = 'CPF'
