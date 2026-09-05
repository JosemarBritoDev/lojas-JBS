from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from compras.models import Fornecedor, PedidoCompra, ItemPedidoCompra


class ItemPedidoCompraInline(TabularInline):
    model = ItemPedidoCompra
    extra = 1
    fields = ("produto", "quantidade", "preco_custo_unitario", "subtotal")


@admin.register(Fornecedor)
class FornecedorAdmin(ModelAdmin):
    list_display = ("razao_social", "nome_fantasia", "cnpj", "telefone", "ativo")
    search_fields = ("razao_social", "nome_fantasia", "cnpj")
    list_filter = ("ativo",)


@admin.register(PedidoCompra)
class PedidoCompraAdmin(ModelAdmin):
    list_display = ("id", "fornecedor", "status", "valor_total", "data_emissao", "data_recebimento")
    search_fields = ("fornecedor__razao_social", "id")
    list_filter = ("status", "data_emissao")
    inlines = [ItemPedidoCompraInline]
    