from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from clientes.models import Cliente, ContaCliente, HistoricoCredito


class HistoricoCreditoInline(TabularInline):
    model = HistoricoCredito
    extra = 0
    readonly_fields = ("tipo", "valor", "descricao", "criado_em")


@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ("nome", "cpf_cnpj", "telefone", "limite_credito", "ativo")
    search_fields = ("nome", "cpf_cnpj")
    list_filter = ("ativo",)


@admin.register(ContaCliente)
class ContaClienteAdmin(ModelAdmin):
    list_display = ("cliente", "saldo_devedor", "limite_disponivel")
    inlines = [HistoricoCreditoInline]