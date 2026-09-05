from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from caixa.models import Caixa, MovimentacaoCaixa


class CaixaService:
    @staticmethod
    @transaction.atomic
    def abrir_caixa(operador, saldo_inicial) -> Caixa:
        saldo_inicial_dec = Decimal(str(saldo_inicial))

        if Caixa.objects.filter(operador=operador, status=Caixa.StatusCaixa.ABERTO).exists():
            raise ValidationError("Já existe um caixa aberto para este operador.")

        return Caixa.objects.create(
            operador=operador,
            saldo_inicial=saldo_inicial_dec,
            saldo_atual=saldo_inicial_dec,
            status=Caixa.StatusCaixa.ABERTO,
        )

    @staticmethod
    @transaction.atomic
    def registrar_movimentacao(
        caixa_id: int, tipo: str, valor, descricao: str, usuario
    ) -> MovimentacaoCaixa:
        valor_dec = Decimal(str(valor))

        if valor_dec <= 0:
            raise ValidationError("O valor da movimentação deve ser maior que zero.")

        caixa = Caixa.objects.select_for_update().get(id=caixa_id)

        if caixa.status != Caixa.StatusCaixa.ABERTO:
            raise ValidationError("Não é possível registrar movimentações em um caixa fechado.")

        if tipo == MovimentacaoCaixa.TipoMovimentacao.SANGRIA:
            if caixa.saldo_atual < valor_dec:
                raise ValidationError("Saldo insuficiente em gaveta para realizar a sangria.")
            caixa.saldo_atual -= valor_dec
        elif tipo in [MovimentacaoCaixa.TipoMovimentacao.SUPRIMENTO, MovimentacaoCaixa.TipoMovimentacao.VENDA]:
            caixa.saldo_atual += valor_dec

        caixa.save()

        return MovimentacaoCaixa.objects.create(
            caixa=caixa, tipo=tipo, valor=valor_dec, descricao=descricao, usuario=usuario
        )

    @staticmethod
    @transaction.atomic
    def fechar_caixa(caixa_id: int, saldo_fechamento_informado) -> Caixa:
        saldo_informado_dec = Decimal(str(saldo_fechamento_informado))
        caixa = Caixa.objects.select_for_update().get(id=caixa_id)

        if caixa.status == Caixa.StatusCaixa.FECHADO:
            raise ValidationError("Este caixa já está fechado.")

        caixa.status = Caixa.StatusCaixa.FECHADO
        caixa.saldo_fechamento_informado = saldo_informado_dec
        caixa.diferenca = saldo_informado_dec - caixa.saldo_atual
        caixa.data_fechamento = timezone.now()
        caixa.save()

        return caixa