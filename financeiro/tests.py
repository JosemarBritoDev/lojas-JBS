from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from financeiro.models import ContaPagar, ContaReceber
from financeiro.services import FinanceiroService


@pytest.mark.django_db
def test_criar_e_pagar_conta_a_pagar():
    conta = FinanceiroService.criar_conta_a_pagar(
        descricao="Aluguel Galpão",
        valor=Decimal("1500.00"),
        data_vencimento="2026-10-10",
    )
    assert conta.status == ContaPagar.StatusConta.PENDENTE

    conta_paga = FinanceiroService.baixar_conta_a_pagar(conta_id=conta.id)
    assert conta_paga.status == ContaPagar.StatusConta.PAGO
    assert conta_paga.data_pagamento is not None


@pytest.mark.django_db
def test_gerar_dre_simples():
    FinanceiroService.criar_conta_a_pagar(
        descricao="Energia Eletrica", valor=Decimal("300.00"), data_vencimento="2026-10-10"
    )
    # Baixar para contar no DRE
    conta = ContaPagar.objects.first()
    FinanceiroService.baixar_conta_a_pagar(conta.id)

    dre = FinanceiroService.calcular_dre()
    assert dre["despesas_totais"] == Decimal("300.00")