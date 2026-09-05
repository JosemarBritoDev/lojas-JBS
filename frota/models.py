from django.db import models


class Veiculo(models.Model):
    placa = models.CharField("Placa", max_length=10, unique=True, db_index=True)
    modelo = models.CharField("Modelo/Marca", max_length=100)
    capacidade_kg = models.IntegerField("Capacidade de Carga (kg)", default=0)
    disponivel = models.BooleanField("Disponível para Rota", default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["modelo"]

    def __str__(self):
        return f"{self.modelo} ({self.placa})"