from django.conf import settings
from django.db import models


class Caixa(models.Model):
    class StatusCaixa(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        FECHADO = "fechado", "Fechado"

    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="caixas",
        verbose_name="Operador",
    )
    status = models.CharField(
        max_length=10,
        choices=StatusCaixa.choices,
        default=StatusCaixa.ABERTO,
        verbose_name="Status",
    )
    saldo_inicial = models.DecimalField(
        "Saldo Inicial", max_digits=10, decimal_places=2, default=0.00
    )
    saldo_atual = models.DecimalField(
        "Saldo Atual em Gaveta", max_digits=10, decimal_places=2, default=0.00
    )
    saldo_fechamento_informado = models.DecimalField(
        "Saldo Contado no Fechamento",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    diferenca = models.DecimalField(
        "Diferença (Sobra/Falta)",
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    data_abertura = models.DateTimeField("Data/Hora de Abertura", auto_now_add=True)
    data_fechamento = models.DateTimeField(
        "Data/Hora de Fechamento", null=True, blank=True
    )

    class Meta:
        verbose_name = "Caixa da Loja"
        verbose_name_plural = "Caixas da Loja"
        ordering = ["-data_abertura"]

    def __str__(self):
        return f"Caixa #{self.id} - {self.operador.username} ({self.get_status_display()})"


class MovimentacaoCaixa(models.Model):
    class TipoMovimentacao(models.TextChoices):
        SUPRIMENTO = "suprimento", "Suprimento (Entrada)"
        SANGRIA = "sangria", "Sangria (Retirada)"
        VENDA = "venda", "Venda de Balcão"

    caixa = models.ForeignKey(
        Caixa,
        on_delete=models.CASCADE,
        related_name="movimentacoes",
        verbose_name="Caixa",
    )
    tipo = models.CharField(
        max_length=20, choices=TipoMovimentacao.choices, verbose_name="Tipo"
    )
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    descricao = models.CharField("Descrição/Motivo", max_length=255)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Responsável",
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimentação de Caixa"
        verbose_name_plural = "Movimentações de Caixa"

    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor}"