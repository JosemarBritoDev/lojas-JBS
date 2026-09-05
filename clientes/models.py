from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Cliente(models.Model):
    nome = models.CharField("Nome do Cliente", max_length=150)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, unique=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    endereco = models.TextField("Endereço Completo", blank=True, null=True)

    limite_credito = models.DecimalField(
        "Limite de Crédito (R$)", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    ativo = models.BooleanField("Ativo", default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.cpf_cnpj})"


class ContaCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente, on_delete=models.CASCADE, related_name="conta", verbose_name="Cliente"
    )
    saldo_devedor = models.DecimalField(
        "Saldo Devedor (R$)", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "Conta do Cliente"
        verbose_name_plural = "Contas dos Clientes"

    def __str__(self):
        return f"Conta {self.cliente.nome} - Devendo: R$ {self.saldo_devedor}"

    @property
    def limite_disponivel(self) -> Decimal:
        return self.cliente.limite_credito - self.saldo_devedor


class HistoricoCredito(models.Model):
    class TipoMovimentacao(models.TextChoices):
        DEBITO = "debito", "Débito (Fiado)"
        PAGAMENTO = "pagamento", "Pagamento (Quitação)"

    conta = models.ForeignKey(
        ContaCliente,
        on_delete=models.CASCADE,
        related_name="historico",
        verbose_name="Conta do Cliente",
    )
    tipo = models.CharField("Tipo", max_length=20, choices=TipoMovimentacao.choices)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    descricao = models.CharField("Descrição/Ref", max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Crédito"
        verbose_name_plural = "Históricos de Crédito"
        ordering = ["-criado_em"]


@receiver(post_save, sender=Cliente)
def criar_conta_cliente(sender, instance, created, **kwargs):
    if created:
        ContaCliente.objects.create(cliente=instance)