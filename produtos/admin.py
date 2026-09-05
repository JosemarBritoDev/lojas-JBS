from django.contrib import admin
from unfold.admin import ModelAdmin
from produtos.models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Produto)
class ProdutoAdmin(ModelAdmin):
    list_display = (
        "nome",
        "codigo_barras",
        "categoria",
        "preco_venda",
        "quantidade_estoque",
        "estoque_minimo",
        "ativo",
    )
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "codigo_barras")