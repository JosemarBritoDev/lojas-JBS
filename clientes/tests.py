from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from clientes.models import Cliente, ContaCliente
from clientes.services import ClienteService


@pytest.fixture
def cliente(db):
    cliente_obj = Cliente.objects.create(
        nome="Carlos Silva",
        cpf_cnpj="123.456.789-01",
        telefone="(11) 98765-4321",
        limite_credito=Decimal("500.00"),
    )
    return cliente_obj


@pytest.mark.django_db
def test_criacao_cliente_com_conta(cliente):
    assert cliente.nome == "Carlos Silva"
    assert hasattr(cliente, "conta")
    assert cliente.conta.saldo_devedor == Decimal("0.00")
    assert cliente.conta.limite_disponivel == Decimal("500.00")
    assert str(cliente) == "Carlos Silva (123.456.789-01)"


@pytest.mark.django_db
def test_registrar_debito_fiado_com_sucesso(cliente):
    conta = ClienteService.registrar_debito_fiado(
        cliente_id=cliente.id, valor=Decimal("150.00"), descricao="Venda no Fiado #10"
    )

    assert conta.saldo_devedor == Decimal("150.00")
    assert conta.limite_disponivel == Decimal("350.00")


@pytest.mark.django_db
def test_impedir_debito_fiado_acima_do_limite(cliente):
    with pytest.raises(ValidationError) as exc_info:
        ClienteService.registrar_debito_fiado(
            cliente_id=cliente.id, valor=Decimal("600.00"), descricao="Venda Fiado Excesso"
        )

    assert "Limite de crédito excedido" in str(exc_info.value)


@pytest.mark.django_db
def test_registrar_pagamento_fiado(cliente):
    ClienteService.registrar_debito_fiado(
        cliente_id=cliente.id, valor=Decimal("200.00"), descricao="Venda no Fiado #11"
    )

    conta = ClienteService.registrar_pagamento(
        cliente_id=cliente.id, valor=Decimal("150.00"), descricao="Pagamento Parcial"
    )

    assert conta.saldo_devedor == Decimal("50.00")
    assert conta.limite_disponivel == Decimal("450.00")