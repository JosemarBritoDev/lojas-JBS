import pytest
from django.core.exceptions import ValidationError
from produtos.models import Categoria, Produto
from produtos.services import ProdutoService


@pytest.mark.django_db
def test_criacao_categoria_e_produto():
    categoria = Categoria.objects.create(nome="Bebidas", slug="bebidas")
    produto = Produto.objects.create(
        nome="Refrigerante 2L",
        codigo_barras="7891234567890",
        categoria=categoria,
        preco_custo=5.00,
        preco_venda=9.50,
        quantidade_estoque=10,
        estoque_minimo=2,
    )

    assert produto.nome == "Refrigerante 2L"
    assert produto.margem_lucro == 4.50
    assert str(produto) == "Refrigerante 2L (7891234567890)"


@pytest.mark.django_db
def test_adicionar_estoque_via_service():
    categoria = Categoria.objects.create(nome="Gás", slug="gas")
    produto = Produto.objects.create(
        nome="Botijão P13",
        codigo_barras="123456",
        categoria=categoria,
        preco_custo=60.00,
        preco_venda=110.00,
        quantidade_estoque=5,
    )

    produto_atualizado = ProdutoService.adicionar_estoque(
        produto_id=produto.id, quantidade=10
    )
    assert produto_atualizado.quantidade_estoque == 15


@pytest.mark.django_db
def test_remover_estoque_com_sucesso():
    categoria = Categoria.objects.create(nome="Gás", slug="gas")
    produto = Produto.objects.create(
        nome="Botijão P13",
        codigo_barras="123456",
        categoria=categoria,
        preco_custo=60.00,
        preco_venda=110.00,
        quantidade_estoque=10,
    )

    produto_atualizado = ProdutoService.remover_estoque(
        produto_id=produto.id, quantidade=4
    )
    assert produto_atualizado.quantidade_estoque == 6


@pytest.mark.django_db
def test_impedir_remocao_estoque_insuficiente():
    categoria = Categoria.objects.create(nome="Gás", slug="gas")
    produto = Produto.objects.create(
        nome="Botijão P13",
        codigo_barras="123456",
        categoria=categoria,
        preco_custo=60.00,
        preco_venda=110.00,
        quantidade_estoque=3,
    )

    with pytest.raises(ValidationError) as exc_info:
        ProdutoService.remover_estoque(produto_id=produto.id, quantidade=5)

    assert "Estoque insuficiente" in str(exc_info.value)