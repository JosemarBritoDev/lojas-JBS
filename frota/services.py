from django.db import transaction
from frota.models import Veiculo


class FrotaService:
    @staticmethod
    @transaction.atomic
    def definir_disponibilidade(veiculo_id: int, disponivel: bool) -> Veiculo:
        veiculo = Veiculo.objects.select_for_update().get(id=veiculo_id)
        veiculo.disponivel = disponivel
        veiculo.save()
        return veiculo