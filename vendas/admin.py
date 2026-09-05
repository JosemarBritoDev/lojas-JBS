from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from vendas.models import ItemVenda, Venda


class ItemVendaInline(TabularInline):
    model = ItemVenda
    extra = 0
    readonly_fields = ("produto", "quantidade", "preco_unitario", "subtotal")


@admin.register(Venda)
class VendaAdmin(ModelAdmin):
    list_display = (
        "id",
        "operador",
        "vendedor",
        "forma_pagamento",
        "valor_total",
        "valor_comissao",
        "criado_em",
    )
    list_filter = ("forma_pagamento", "criado_em")
    inlines = [ItemVendaInline]