from django.core.exceptions import ValidationError
from django.db import transaction
from produtos.models import Produto


class ProdutoService:
    @staticmethod
    @transaction.atomic
    def adicionar_estoque(produto_id: int, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise ValidationError("A quantidade a ser adicionada deve ser maior que zero.")

        produto = Produto.objects.select_for_update().get(id=produto_id)
        produto.quantidade_estoque += quantidade
        produto.save()
        return produto

    @staticmethod
    @transaction.atomic
    def remover_estoque(produto_id: int, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise ValidationError("A quantidade a ser removida deve ser maior que zero.")

        produto = Produto.objects.select_for_update().get(id=produto_id)

        if produto.quantidade_estoque < quantidade:
            raise ValidationError(
                f"Estoque insuficiente para {produto.nome}. "
                f"Disponível: {produto.quantidade_estoque}, Solicitado: {quantidade}"
            )

        produto.quantidade_estoque -= quantidade
        produto.save()
        return produto