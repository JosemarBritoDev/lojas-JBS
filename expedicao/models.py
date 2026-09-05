from django.db import models
from frota.models import Veiculo
from funcionarios.models import Funcionario
from vendas.models import Venda


class OrdemEntrega(models.Model):
    class StatusEntrega(models.TextChoices):
        SEPARACAO = "separacao", "Em Separação"
        EM_ROTA = "em_rota", "Em Rota de Entrega"
        ENTREGUE = "entregue", "Entregue"
        CANCELADO = "cancelado", "Cancelada"

    venda = models.OneToOneField(
        Venda,
        on_delete=models.CASCADE,
        related_name="ordem_entrega",
        verbose_name="Venda Relacionada",
    )
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        verbose_name="Veículo Alocado",
    )
    entregador = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entregas",
        verbose_name="Entregador/Motorista",
    )

    endereco_destino = models.TextField("Endereço de Entrega")
    status = models.CharField(
        "Status da Entrega",
        max_length=20,
        choices=StatusEntrega.choices,
        default=StatusEntrega.SEPARACAO,
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField("Data/Hora de Saída", null=True, blank=True)
    data_conclusao = models.DateTimeField("Data/Hora de Conclusão", null=True, blank=True)

    class Meta:
        verbose_name = "Ordem de Entrega"
        verbose_name_plural = "Ordens de Entrega"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Entrega #{self.id} - Venda #{self.venda.id} ({self.get_status_display()})"