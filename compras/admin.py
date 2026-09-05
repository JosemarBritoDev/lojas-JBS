from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline
from compras.models import Fornecedor, PedidoCompra, ItemPedidoCompra
from compras.services import CompraService


class ItemPedidoCompraInline(TabularInline):
    model = ItemPedidoCompra
    extra = 1


@admin.register(Fornecedor)
class FornecedorAdmin(ModelAdmin):
    list_display = ("nome_fantasia", "razao_social", "cnpj", "telefone", "ativo")
    search_fields = ("nome_fantasia", "razao_social", "cnpj")


@admin.register(PedidoCompra)
class PedidoCompraAdmin(ModelAdmin):
    list_display = ("id", "fornecedor", "status", "valor_total", "data_emissao", "data_recebimento")
    list_filter = ("status",)
    search_fields = ("fornecedor__nome_fantasia", "fornecedor__cnpj")
    inlines = [ItemPedidoCompraInline]
    actions = ["marcar_como_entregue"]

    @admin.action(description="Marcar pedidos selecionados como ENTREGUE (Dar entrada no estoque)")
    def marcar_como_entregue(self, request, queryset):
        for pedido in queryset:
            try:
                CompraService.receber_pedido_compra(pedido_id=pedido.id)
                self.message_user(
                    request,
                    f"Pedido #{pedido.id} marcado como ENTREGUE com sucesso e estoque atualizado!",
                    messages.SUCCESS,
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Erro ao processar recebimento do Pedido #{pedido.id}: {str(e)}",
                    messages.ERROR,
                )