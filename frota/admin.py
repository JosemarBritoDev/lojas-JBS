from django.contrib import admin
from unfold.admin import ModelAdmin
from frota.models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(ModelAdmin):
    list_display = ("placa", "modelo", "capacidade_kg", "disponivel")
    search_fields = ("placa", "modelo")
    list_filter = ("disponivel",)