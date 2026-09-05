from decimal import Decimal
from django.db import models
from produtos.models import Produto


class Fornecedor(models.Model):
    razao_social = models.CharField("Razão Social", max_length=150)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=150, blank=True, null=True)
    cnpj = models.CharField("CNPJ", max_length=20, unique=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    endereco = models.TextField("Endereço Completo", blank=True, null=True)
    ativo = models.BooleanField("Ativo", default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["razao_social"]

    def __str__(self):
        nome = self.nome_fantasia or self.razao_social
        return f"{nome} ({self.cnpj})"


class PedidoCompra(models.Model):
    class StatusPedido(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        CONFIRMADO = "confirmado", "Confirmado"
        RECEBIDO = "recebido", "Recebido / Entregue"
        CANCELADO = "cancelado", "Cancelado"

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name="pedidos_compra",
        verbose_name="Fornecedor",
    )
    status = models.CharField(
        "Status",
        max_length=20,
        choices=StatusPedido.choices,
        default=StatusPedido.RASCUNHO,
    )
    valor_total = models.DecimalField(
        "Valor Total (R$)", max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    observacao = models.TextField("Observações", blank=True, null=True)

    data_emissao = models.DateTimeField("Data de Emissão", auto_now_add=True)
    data_recebimento = models.DateTimeField("Data de Recebimento", blank=True, null=True)

    class Meta:
        verbose_name = "Pedido de Compra"
        verbose_name_plural = "Pedidos de Compra"
        ordering = ["-data_emissao"]

    def __str__(self):
        return f"Pedido #{self.id} - {self.fornecedor.razao_social} ({self.get_status_display()})"


class ItemPedidoCompra(models.Model):
    pedido = models.ForeignKey(
        PedidoCompra,
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Pedido de Compra",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_compra",
        verbose_name="Produto",
    )
    quantidade = models.PositiveIntegerField("Quantidade Comprada")
    preco_custo_unitario = models.DecimalField("Preço de Custo Unitário (R$)", max_digits=10, decimal_places=2)
    subtotal = models.DecimalField("Subtotal (R$)", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item do Pedido de Compra"
        verbose_name_plural = "Itens do Pedido de Compra"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (R$ {self.subtotal})"