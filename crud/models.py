from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=30)
    idade = models.PositiveIntegerField()
    telefone = models.CharField(max_length=11)
    email = models.EmailField(max_length=80)
    qtd_pessoas = models.PositiveIntegerField()
    cpf = models.CharField(
        max_length=14,
        unique=True,  # ✅ CPF continua único e totalmente integrado ao admin
        blank=True,
        null=True
    )
    prato_selecionado = models.CharField(  # ✅ campo adicionado
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class Avaliacao(models.Model):
    pessoa = models.ForeignKey(
        'Pessoa',
        on_delete=models.CASCADE,  # ✅ mantém coerência no inline admin
        related_name='avaliacoes',
        null=True,
        blank=True
    )
    comentario = models.TextField(max_length=200)
    nota = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pessoa.nome if self.pessoa else "Sem pessoa"} - {self.comentario[:50]}'
