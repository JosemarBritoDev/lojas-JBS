from decimal import Decimal
from django.conf import settings
from django.db import models
from caixa.models import Caixa
from clientes.models import Cliente
from funcionarios.models import Funcionario


class Venda(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "dinheiro", "Dinheiro"
        PIX = "pix", "PIX"
        CARTAO_DEBITO = "debito", "Cartão de Débito"
        CARTAO_CREDITO = "credito", "Cartão de Crédito"
        FIADO = "fiado", "Fiado / Crédito"

    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vendas_operadas",
        verbose_name="Operador do Caixa",
    )
    vendedor = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name="vendas_realizadas",
        verbose_name="Vendedor",
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vendas",
        verbose_name="Cliente",
    )
    caixa = models.ForeignKey(
        Caixa,
        on_delete=models.PROTECT,
        related_name="vendas",
        verbose_name="Caixa",
    )

    forma_pagamento = models.CharField(
        "Forma de Pagamento", max_length=20, choices=FormaPagamento.choices
    )
    valor_total = models.DecimalField(
        "Valor Total (R$)", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    valor_comissao = models.DecimalField(
        "Valor Comissão (R$)", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Venda #{self.id} - R$ {self.valor_total}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE, related_name="itens", verbose_name="Venda"
    )
    produto = models.ForeignKey(
        "produtos.Produto",
        on_delete=models.PROTECT,
        related_name="itens_vendidos",
        verbose_name="Produto",
    )
    quantidade = models.PositiveIntegerField("Quantidade")
    preco_unitario = models.DecimalField(
        "Preço Unitário (R$)", max_digits=10, decimal_places=2
    )
    subtotal = models.DecimalField("Subtotal (R$)", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (R$ {self.subtotal})"