from decimal import Decimal
import pytest
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from caixa.models import Caixa
from caixa.services import CaixaService
from funcionarios.models import Cargo, Funcionario
from produtos.models import Categoria, Produto
from vendas.models import Venda
from vendas.services import VendaService


@pytest.fixture
def ambiente_vendas(db):
    user = User.objects.create_user(username="vendedor1", password="123")
    # Criação do objeto Group real para garantir integridade relacional
    grupo = Group.objects.create(name="Vendedores_Test")
    cargo = Cargo.objects.create(nome="Vendedor", grupo_django=grupo)
    func = Funcionario.objects.create(
        user=user,
        cargo=cargo,
        cpf="111.222.333-44",
        comissao_percentual=Decimal("5.00"),
    )
    cat = Categoria.objects.create(nome="Geral", slug="geral")
    prod = Produto.objects.create(
        nome="Produto Teste",
        codigo_barras="789000",
        categoria=cat,
        preco_custo=Decimal("10.00"),
        preco_venda=Decimal("20.00"),
        quantidade_estoque=10,
    )
    caixa = CaixaService.abrir_caixa(operador=user, saldo_inicial=Decimal("100.00"))
    return {"user": user, "funcionario": func, "produto": prod, "caixa": caixa}


@pytest.mark.django_db
def test_realizar_venda_pdv_com_sucesso(ambiente_vendas):
    env = ambiente_vendas
    itens = [{"produto_id": env["produto"].id, "quantidade": 2}]

    venda = VendaService.realizar_venda(
        operador=env["user"],
        vendedor=env["funcionario"],
        caixa=env["caixa"],
        itens_data=itens,
        forma_pagamento=Venda.FormaPagamento.DINHEIRO,
    )

    env["produto"].refresh_from_db()
    env["caixa"].refresh_from_db()

    assert venda.valor_total == Decimal("40.00")
    assert venda.valor_comissao == Decimal("2.00")
    assert env["produto"].quantidade_estoque == 8
    assert env["caixa"].saldo_atual == Decimal("140.00")


@pytest.mark.django_db
def test_impedir_venda_com_estoque_insuficiente(ambiente_vendas):
    env = ambiente_vendas
    itens = [{"produto_id": env["produto"].id, "quantidade": 20}]

    with pytest.raises(ValidationError) as exc_info:
        VendaService.realizar_venda(
            operador=env["user"],
            vendedor=env["funcionario"],
            caixa=env["caixa"],
            itens_data=itens,
            forma_pagamento=Venda.FormaPagamento.DINHEIRO,
        )

    assert "Estoque insuficiente" in str(exc_info.value)