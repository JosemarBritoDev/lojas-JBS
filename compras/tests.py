from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from compras.models import Fornecedor, PedidoCompra
from compras.services import CompraService
from produtos.models import Categoria, Produto


@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(
        razao_social="Distribuidora de Alimentos Silva LTDA",
        nome_fantasia="Distribuidora Silva",
        cnpj="12.345.678/0001-90",
        telefone="(11) 3333-4444",
        email="vendas@distribuidorasilva.com.br",
    )


@pytest.fixture
def produto(db):
    categoria = Categoria.objects.create(nome="Bebidas", slug="bebidas")
    return Produto.objects.create(
        nome="Refrigerante Cola 2L",
        codigo_barras="7891112223334",
        preco_custo=Decimal("4.00"),
        preco_venda=Decimal("8.00"),
        quantidade_estoque=10,
        estoque_minimo=5,
        categoria=categoria,
    )


@pytest.mark.django_db
def test_criacao_fornecedor(fornecedor):
    assert fornecedor.razao_social == "Distribuidora de Alimentos Silva LTDA"
    assert str(fornecedor) == "Distribuidora Silva (12.345.678/0001-90)"


@pytest.mark.django_db
def test_criar_pedido_compra(fornecedor, produto):
    itens = [{"produto_id": produto.id, "quantidade": 50, "preco_custo_unitario": Decimal("4.50")}]

    pedido = CompraService.criar_pedido_compra(
        fornecedor_id=fornecedor.id, itens=itens, observacao="Reposição de estoque semanal"
    )

    assert pedido.status == PedidoCompra.StatusPedido.RASCUNHO
    assert pedido.valor_total == Decimal("225.00")
    assert pedido.itens.count() == 1

    produto.refresh_from_db()
    assert produto.quantidade_estoque == 10


@pytest.mark.django_db
def test_receber_pedido_compra_atualiza_estoque_e_custo(fornecedor, produto):
    itens = [{"produto_id": produto.id, "quantidade": 20, "preco_custo_unitario": Decimal("5.00")}]

    pedido = CompraService.criar_pedido_compra(fornecedor_id=fornecedor.id, itens=itens)
    pedido_recebido = CompraService.receber_pedido_compra(pedido_id=pedido.id)

    assert pedido_recebido.status == PedidoCompra.StatusPedido.RECEBIDO

    produto.refresh_from_db()
    assert produto.quantidade_estoque == 30
    assert produto.preco_custo == Decimal("5.00")


@pytest.mark.django_db
def test_impedir_recebimento_duplicado_de_pedido(fornecedor, produto):
    itens = [{"produto_id": produto.id, "quantidade": 10, "preco_custo_unitario": Decimal("4.00")}]

    pedido = CompraService.criar_pedido_compra(fornecedor_id=fornecedor.id, itens=itens)
    CompraService.receber_pedido_compra(pedido_id=pedido.id)

    with pytest.raises(ValidationError) as exc_info:
        CompraService.receber_pedido_compra(pedido_id=pedido.id)

    assert "Apenas pedidos com status 'Rascunho' ou 'Confirmado' podem ser recebidos" in str(
        exc_info.value
    )