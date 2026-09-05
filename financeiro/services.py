from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from financeiro.models import ContaPagar, ContaReceber
from vendas.models import Venda


class FinanceiroService:
    @staticmethod
    @transaction.atomic
    def criar_conta_a_pagar(descricao: str, valor: Decimal, data_vencimento: str) -> ContaPagar:
        return ContaPagar.objects.create(
            descricao=descricao, valor=Decimal(str(valor)), data_vencimento=data_vencimento
        )

    @staticmethod
    @transaction.atomic
    def baixar_conta_a_pagar(conta_id: int) -> ContaPagar:
        conta = ContaPagar.objects.select_for_update().get(id=conta_id)
        if conta.status == ContaPagar.StatusConta.PAGO:
            raise ValidationError("Esta conta já foi paga.")

        conta.status = ContaPagar.StatusConta.PAGO
        conta.data_pagamento = timezone.now().date()
        conta.save()
        return conta

    @staticmethod
    def calcular_dre() -> dict:
        receita_vendas = Venda.objects.aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")
        outras_receitas = ContaReceber.objects.filter(
            status=ContaReceber.StatusConta.RECEBIDO
        ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

        despesas = ContaPagar.objects.filter(
            status=ContaPagar.StatusConta.PAGO
        ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")

        receita_bruta = receita_vendas + outras_receitas
        lucro_liquido = receita_bruta - despesas

        return {
            "receita_bruta": receita_bruta,
            "despesas_totais": despesas,
            "lucro_liquido": lucro_liquido,
        }