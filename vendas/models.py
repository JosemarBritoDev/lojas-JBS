from decimal import Decimal
from django.conf import settings
from django.db import models
from caixa.models import Caixa
from funcionarios.models import Funcionario
from produtos.models import Produto


class Venda(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "dinheiro", "Dinheiro"
        PIX = "pix", "PIX"
        CARTAO_DEBITO = "debito", "Cartão de Débito"
        CARTAO_CREDITO = "credito", "Cartão de Crédito"
        FIADO = "fiado", "Fiado / Conta Cliente"

    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Operador do PDV"
    )
    vendedor = models.ForeignKey(
        Funcionario, on_delete=models.PROTECT, verbose_name="Vendedor Responsável"
    )
    caixa = models.ForeignKey(
        Caixa, on_delete=models.PROTECT, related_name="vendas", verbose_name="Caixa"
    )

    forma_pagamento = models.CharField(
        max_length=20, choices=FormaPagamento.choices, verbose_name="Forma de Pagamento"
    )
    valor_total = models.DecimalField("Valor Total", max_digits=10, decimal_places=2, default=0.00)
    valor_comissao = models.DecimalField(
        "Comissão do Vendedor", max_digits=10, decimal_places=2, default=0.00
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
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name="Produto")
    quantidade = models.IntegerField("Quantidade")
    preco_unitario = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Venda #{self.venda.id})"