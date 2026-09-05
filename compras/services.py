from decimal import Decimal
from typing import List, Dict, Any
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from compras.models import Fornecedor, PedidoCompra, ItemPedidoCompra
from produtos.models import Produto
from produtos.services import ProdutoService


class CompraService:
    @staticmethod
    @transaction.atomic
    def criar_pedido_compra(fornecedor_id: int, itens: List[Dict[str, Any]], observacao: str = "") -> PedidoCompra:
        if not itens:
            raise ValidationError("O pedido de compra deve conter ao menos um item.")

        fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        pedido = PedidoCompra.objects.create(
            fornecedor=fornecedor,
            observacao=observacao,
            status=PedidoCompra.StatusPedido.RASCUNHO,
        )

        valor_total = Decimal("0.00")

        for item_data in itens:
            produto = Produto.objects.get(id=item_data["produto_id"])
            qtd = int(item_data["quantidade"])
            preco_custo = Decimal(str(item_data["preco_custo_unitario"]))

            if qtd <= 0:
                raise ValidationError("A quantidade comprada deve ser maior que zero.")

            subtotal = qtd * preco_custo
            valor_total += subtotal

            ItemPedidoCompra.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=qtd,
                preco_custo_unitario=preco_custo,
                subtotal=subtotal,
            )

        pedido.valor_total = valor_total
        pedido.save()

        return pedido

    @staticmethod
    @transaction.atomic
    def receber_pedido_compra(pedido_id: int) -> PedidoCompra:
        pedido = PedidoCompra.objects.select_for_update().prefetch_related("itens__produto").get(id=pedido_id)

        if pedido.status in [PedidoCompra.StatusPedido.RECEBIDO, PedidoCompra.StatusPedido.CANCELADO]:
            raise ValidationError(
                "Apenas pedidos com status 'Rascunho' ou 'Confirmado' podem ser recebidos."
            )

        for item in pedido.itens.all():
            # Atualiza o preço de custo no produto
            produto = item.produto
            produto.preco_custo = item.preco_custo_unitario
            produto.save()

            # Adiciona ao estoque via ProdutoService
            ProdutoService.adicionar_estoque(produto_id=produto.id, quantidade=item.quantidade)

        pedido.status = PedidoCompra.StatusPedido.RECEBIDO
        pedido.data_recebimento = timezone.now()
        pedido.save()

        return pedido