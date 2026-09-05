from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from clientes.models import Cliente, ContaCliente, HistoricoCredito


class ClienteService:
    @staticmethod
    @transaction.atomic
    def registrar_debito_fiado(cliente_id: int, valor: Decimal, descricao: str) -> ContaCliente:
        valor_dec = Decimal(str(valor))
        if valor_dec <= Decimal("0.00"):
            raise ValidationError("O valor do débito deve ser maior que zero.")

        cliente = Cliente.objects.select_related("conta").get(id=cliente_id)
        conta = cliente.conta

        if conta.limite_disponivel < valor_dec:
            raise ValidationError(
                f"Limite de crédito excedido. Limite disponível: R$ {conta.limite_disponivel}"
            )

        conta.saldo_devedor += valor_dec
        conta.save()

        HistoricoCredito.objects.create(
            conta=conta,
            tipo=HistoricoCredito.TipoMovimentacao.DEBITO,
            valor=valor_dec,
            descricao=descricao,
        )

        return conta

    @staticmethod
    @transaction.atomic
    def registrar_pagamento(cliente_id: int, valor: Decimal, descricao: str) -> ContaCliente:
        valor_dec = Decimal(str(valor))
        if valor_dec <= Decimal("0.00"):
            raise ValidationError("O valor do pagamento deve ser maior que zero.")

        cliente = Cliente.objects.select_related("conta").get(id=cliente_id)
        conta = cliente.conta

        if valor_dec > conta.saldo_devedor:
            raise ValidationError(
                f"O valor informado (R$ {valor_dec}) é maior que o saldo devedor atual (R$ {conta.saldo_devedor})."
            )

        conta.saldo_devedor -= valor_dec
        conta.save()

        HistoricoCredito.objects.create(
            conta=conta,
            tipo=HistoricoCredito.TipoMovimentacao.PAGAMENTO,
            valor=valor_dec,
            descricao=descricao,
        )

        return conta