from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from caixa.models import MovimentacaoCaixa
from caixa.services import CaixaService
from produtos.services import ProdutoService
from vendas.models import ItemVenda, Venda


class VendaService:
    @staticmethod
    @transaction.atomic
    def realizar_venda(
        operador, vendedor, caixa, itens_data: list, forma_pagamento: str
    ) -> Venda:
        if not itens_data:
            raise ValidationError("A venda precisa ter ao menos um item.")

        venda = Venda.objects.create(
            operador=operador,
            vendedor=vendedor,
            caixa=caixa,
            forma_pagamento=forma_pagamento,
            valor_total=Decimal("0.00"),
        )

        total_venda = Decimal("0.00")

        for item_info in itens_data:
            prod_id = item_info["produto_id"]
            qtd = item_info["quantidade"]

            # 1. Baixa no Estoque via ProdutoService
            produto = ProdutoService.remover_estoque(
                produto_id=prod_id, quantidade=qtd
            )
            subtotal = produto.preco_venda * Decimal(str(qtd))

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=qtd,
                preco_unitario=produto.preco_venda,
                subtotal=subtotal,
            )

            total_venda += subtotal

        # 2. Calcular comissão do vendedor
        comissao = (total_venda * vendedor.comissao_percentual) / Decimal("100.00")

        venda.valor_total = total_venda
        venda.valor_comissao = comissao
        venda.save()

        # 3. Lançamento no Caixa (se o pagamento for em dinheiro ou PIX)
        if forma_pagamento in [
            Venda.FormaPagamento.DINHEIRO,
            Venda.FormaPagamento.PIX,
        ]:
            CaixaService.registrar_movimentacao(
                caixa_id=caixa.id,
                tipo=MovimentacaoCaixa.TipoMovimentacao.VENDA,
                valor=total_venda,
                descricao=f"Venda #{venda.id} - Balcão/PDV",
                usuario=operador,
            )

        return venda