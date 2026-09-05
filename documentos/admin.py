from django.contrib import admin
from unfold.admin import ModelAdmin
from documentos.models import CategoriaDocumento, Documento


@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(ModelAdmin):
    list_display = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Documento)
class DocumentoAdmin(ModelAdmin):
    list_display = ("titulo", "categoria", "enviado_por", "criado_em")
    list_filter = ("categoria", "criado_em")
    search_fields = ("titulo",)
    filter_horizontal = ("grupos_permitidos",)