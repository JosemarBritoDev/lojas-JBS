from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from expedicao.models import OrdemEntrega
from frota.models import Veiculo
from frota.services import FrotaService
from funcionarios.models import Funcionario
from vendas.models import Venda


class ExpedicaoService:
    @staticmethod
    @transaction.atomic
    def criar_ordem_entrega(venda_id: int, endereco_destino: str) -> OrdemEntrega:
        venda = Venda.objects.get(id=venda_id)
        return OrdemEntrega.objects.create(
            venda=venda,
            endereco_destino=endereco_destino,
            status=OrdemEntrega.StatusEntrega.SEPARACAO,
        )

    @staticmethod
    @transaction.atomic
    def despachar_entrega(
        ordem_id: int, veiculo_id: int, entregador_id: int
    ) -> OrdemEntrega:
        ordem = OrdemEntrega.objects.select_for_update().get(id=ordem_id)
        veiculo = Veiculo.objects.get(id=veiculo_id)
        entregador = Funcionario.objects.get(id=entregador_id)

        if not veiculo.disponivel:
            raise ValidationError(f"O veículo {veiculo.placa} não está disponível para rota.")

        if ordem.status != OrdemEntrega.StatusEntrega.SEPARACAO:
            raise ValidationError("Apenas ordens em separação podem ser despachadas.")

        # Ocupa veículo
        FrotaService.definir_disponibilidade(veiculo_id=veiculo.id, disponivel=False)

        ordem.veiculo = veiculo
        ordem.entregador = entregador
        ordem.status = OrdemEntrega.StatusEntrega.EM_ROTA
        ordem.data_saida = timezone.now()
        ordem.save()

        return ordem

    @staticmethod
    @transaction.atomic
    def concluir_entrega(ordem_id: int) -> OrdemEntrega:
        ordem = OrdemEntrega.objects.select_for_update().get(id=ordem_id)

        if ordem.status != OrdemEntrega.StatusEntrega.EM_ROTA:
            raise ValidationError("Apenas ordens em rota podem ser concluídas.")

        # Libera veículo
        if ordem.veiculo:
            FrotaService.definir_disponibilidade(
                veiculo_id=ordem.veiculo.id, disponivel=True
            )

        ordem.status = OrdemEntrega.StatusEntrega.ENTREGUE
        ordem.data_conclusao = timezone.now()
        ordem.save()

        return ordem