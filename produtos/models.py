from django.db import models


class Categoria(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)
    slug = models.SlugField("Slug", unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos",
        verbose_name="Categoria",
    )
    nome = models.CharField("Nome do Produto", max_length=150)
    codigo_barras = models.CharField(
        "Código de Barras", max_length=50, unique=True, db_index=True
    )
    descricao = models.TextField("Descrição", blank=True, null=True)

    preco_custo = models.DecimalField(
        "Preço de Custo", max_digits=10, decimal_places=2
    )
    preco_venda = models.DecimalField(
        "Preço de Venda", max_digits=10, decimal_places=2
    )

    quantidade_estoque = models.IntegerField("Quantidade em Estoque", default=0)
    estoque_minimo = models.IntegerField("Estoque Mínimo", default=1)
    ativo = models.BooleanField("Ativo", default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.nome} ({self.codigo_barras})"

    @property
    def margem_lucro(self):
        return self.preco_venda - self.preco_custo

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo