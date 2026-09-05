from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from caixa.models import Caixa, MovimentacaoCaixa


class MovimentacaoCaixaInline(TabularInline):
    model = MovimentacaoCaixa
    extra = 0
    readonly_fields = ("tipo", "valor", "descricao", "usuario", "criado_em")


@admin.register(Caixa)
class CaixaAdmin(ModelAdmin):
    list_display = (
        "id",
        "operador",
        "status",
        "saldo_inicial",
        "saldo_atual",
        "saldo_fechamento_informado",
        "diferenca",
        "data_abertura",
    )
    list_filter = ("status", "data_abertura")
    inlines = [MovimentacaoCaixaInline]