from decimal import Decimal
from django.db import models


class ContaPagar(models.Model):
    class StatusConta(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        PAGO = "pago", "Pago"
        CANCELADO = "cancelado", "Cancelado"

    descricao = models.CharField("Descrição", max_length=200)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    data_vencimento = models.DateField("Data de Vencimento")
    data_pagamento = models.DateField("Data do Pagamento", null=True, blank=True)
    status = models.CharField(
        "Status", max_length=20, choices=StatusConta.choices, default=StatusConta.PENDENTE
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ["data_vencimento"]

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


class ContaReceber(models.Model):
    class StatusConta(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        RECEBIDO = "recebido", "Recebido"
        CANCELADO = "cancelado", "Cancelado"

    descricao = models.CharField("Descrição", max_length=200)
    valor = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    data_vencimento = models.DateField("Data de Vencimento")
    data_recebimento = models.DateField("Data de Recebimento", null=True, blank=True)
    status = models.CharField(
        "Status", max_length=20, choices=StatusConta.choices, default=StatusConta.PENDENTE
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ["data_vencimento"]

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"