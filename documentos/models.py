import os
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models


def caminho_documento(instance, filename):
    return os.path.join("documentos", instance.categoria.slug, filename)


class CategoriaDocumento(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Categoria de Documento"
        verbose_name_plural = "Categorias de Documentos"

    def __str__(self):
        return self.nome


class Documento(models.Model):
    titulo = models.CharField("Título", max_length=200)
    arquivo = models.FileField("Arquivo", upload_to=caminho_documento)
    categoria = models.ForeignKey(
        CategoriaDocumento, on_delete=models.PROTECT, verbose_name="Categoria"
    )
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Enviado Por"
    )
    grupos_permitidos = models.ManyToManyField(
        Group, blank=True, verbose_name="Cargos/Grupos Autorizados"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.titulo