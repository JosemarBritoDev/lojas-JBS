from django.contrib import admin
from unfold.admin import ModelAdmin
from financeiro.models import ContaPagar, ContaReceber


@admin.register(ContaPagar)
class ContaPagarAdmin(ModelAdmin):
    list_display = ("descricao", "valor", "data_vencimento", "status", "data_pagamento")
    list_filter = ("status", "data_vencimento")
    search_fields = ("descricao",)


@admin.register(ContaReceber)
class ContaReceberAdmin(ModelAdmin):
    list_display = ("descricao", "valor", "data_vencimento", "status", "data_recebimento")
    list_filter = ("status", "data_vencimento")
    search_fields = ("descricao",)