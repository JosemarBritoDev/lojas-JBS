from django.contrib.auth.models import Group, User
from django.db import models


class Cargo(models.Model):
    nome = models.CharField("Nome da Função", max_length=100, unique=True)
    grupo_django = models.OneToOneField(
        Group, on_delete=models.CASCADE, verbose_name="Grupo de Permissões"
    )
    descricao = models.TextField("Atribuições", blank=True, null=True)

    class Meta:
        verbose_name = "Cargo / Função"
        verbose_name_plural = "Cargos e Funções"

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="funcionario"
    )
    cargo = models.ForeignKey(
        Cargo, on_delete=models.PROTECT, verbose_name="Função"
    )
    cpf = models.CharField("CPF", max_length=14, unique=True)
    comissao_percentual = models.DecimalField(
        "Comissão (%)", max_digits=5, decimal_places=2, default=0.00
    )
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        nome = self.user.get_full_name() or self.user.username
        return f"{nome} - {self.cargo.nome}"
