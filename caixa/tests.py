from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from caixa.models import Caixa, MovimentacaoCaixa
from caixa.services import CaixaService


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="operador", password="123")


@pytest.mark.django_db
def test_abrir_caixa_com_sucesso(usuario):
    caixa = CaixaService.abrir_caixa(operador=usuario, saldo_inicial=Decimal("100.00"))

    assert caixa.status == Caixa.StatusCaixa.ABERTO
    assert caixa.saldo_inicial == Decimal("100.00")
    assert caixa.saldo_atual == Decimal("100.00")


@pytest.mark.django_db
def test_impedir_abrir_segundo_caixa_para_mesmo_operador(usuario):
    CaixaService.abrir_caixa(operador=usuario, saldo_inicial=Decimal("100.00"))

    with pytest.raises(ValidationError) as exc_info:
        CaixaService.abrir_caixa(operador=usuario, saldo_inicial=Decimal("50.00"))

    assert "Já existe um caixa aberto" in str(exc_info.value)


@pytest.mark.django_db
def test_registrar_suprimento_e_sangria(usuario):
    caixa = CaixaService.abrir_caixa(operador=usuario, saldo_inicial=Decimal("100.00"))

    # Suprimento (+ R$ 50,00 troco)
    CaixaService.registrar_movimentacao(
        caixa_id=caixa.id,
        tipo=MovimentacaoCaixa.TipoMovimentacao.SUPRIMENTO,
        valor=Decimal("50.00"),
        descricao="Troco adicional",
        usuario=usuario,
    )
    caixa.refresh_from_db()
    assert caixa.saldo_atual == Decimal("150.00")

    # Sangria (- R$ 30,00 recolhimento)
    CaixaService.registrar_movimentacao(
        caixa_id=caixa.id,
        tipo=MovimentacaoCaixa.TipoMovimentacao.SANGRIA,
        valor=Decimal("30.00"),
        descricao="Recolhimento para o cofre",
        usuario=usuario,
    )
    caixa.refresh_from_db()
    assert caixa.saldo_atual == Decimal("120.00")


@pytest.mark.django_db
def test_fechar_caixa_com_sucesso(usuario):
    caixa = CaixaService.abrir_caixa(operador=usuario, saldo_inicial=Decimal("100.00"))
    caixa_fechado = CaixaService.fechar_caixa(
        caixa_id=caixa.id, saldo_fechamento_informado=Decimal("100.00")
    )

    assert caixa_fechado.status == Caixa.StatusCaixa.FECHADO
    assert caixa_fechado.diferenca == Decimal("0.00")