from django.contrib import admin
from unfold.admin import ModelAdmin
from funcionarios.models import Cargo, Funcionario


@admin.register(Cargo)
class CargoAdmin(ModelAdmin):
    list_display = ("nome", "grupo_django", "descricao")
    search_fields = ("nome",)


@admin.register(Funcionario)
class FuncionarioAdmin(ModelAdmin):
    list_display = ("user", "cargo", "cpf", "comissao_percentual", "ativo")
    list_filter = ("cargo", "ativo")
    search_fields = ("user__username", "user__first_name", "cpf")