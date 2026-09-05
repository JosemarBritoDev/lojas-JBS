from django.contrib import admin
from unfold.admin import ModelAdmin
from expedicao.models import OrdemEntrega


@admin.register(OrdemEntrega)
class OrdemEntregaAdmin(ModelAdmin):
    list_display = (
        "id",
        "venda",
        "veiculo",
        "entregador",
        "status",
        "data_saida",
        "data_conclusao",
    )
    list_filter = ("status", "data_criacao")
    search_fields = ("venda__id", "endereco_destino")