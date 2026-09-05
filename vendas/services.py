from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from caixa.models import MovimentacaoCaixa
from caixa.services import CaixaService
from clientes.models import Cliente
from clientes.services import ClienteService
from produtos.services import ProdutoService
from vendas.models import ItemVenda, Venda


class VendaService:
    @staticmethod
    @transaction.atomic
    def realizar_venda(
        operador, vendedor, caixa, itens_data: list, forma_pagamento: str, cliente_id: int = None
    ) -> Venda:
        if not itens_data:
            raise ValidationError("A venda precisa ter ao menos um item.")

        cliente = None
        if cliente_id:
            cliente = Cliente.objects.get(id=cliente_id)

        # Validação para venda no Fiado
        if forma_pagamento == Venda.FormaPagamento.FIADO and not cliente:
            raise ValidationError("É obrigatório selecionar um cliente cadastrado para vendas no Fiado.")

        venda = Venda.objects.create(
            operador=operador,
            vendedor=vendedor,
            cliente=cliente,
            caixa=caixa,
            forma_pagamento=forma_pagamento,
            valor_total=Decimal("0.00"),
        )

        total_venda = Decimal("0.00")

        for item_info in itens_data:
            prod_id = item_info["produto_id"]
            qtd = item_info["quantidade"]

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

        comissao = (total_venda * vendedor.comissao_percentual) / Decimal("100.00")

        venda.valor_total = total_venda
        venda.valor_comissao = comissao
        venda.save()

        # Tratamento de Fluxo Financeiro por Forma de Pagamento
        if forma_pagamento in [
            Venda.FormaPagamento.DINHEIRO,
            Venda.FormaPagamento.PIX,
            Venda.FormaPagamento.CARTAO_DEBITO,
            Venda.FormaPagamento.CARTAO_CREDITO,
        ]:
            # Entra no registro de movimentações para conferência do caixa
            CaixaService.registrar_movimentacao(
                caixa_id=caixa.id,
                tipo=MovimentacaoCaixa.TipoMovimentacao.VENDA,
                valor=total_venda,
                descricao=f"Venda #{venda.id} - PDV [{forma_pagamento.upper()}]",
                usuario=operador,
            )
        elif forma_pagamento == Venda.FormaPagamento.FIADO:
            # Não entra no saldo do caixa agora, gera o débito na conta do cliente
            ClienteService.registrar_debito_fiado(
                cliente_id=cliente.id,
                valor=total_venda,
                descricao=f"Venda no Fiado #{venda.id} - PDV",
            )

        return venda