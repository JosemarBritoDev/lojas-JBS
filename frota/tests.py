import pytest
from django.core.exceptions import ValidationError
from frota.models import Veiculo
from frota.services import FrotaService


@pytest.fixture
def veiculo(db):
    return Veiculo.objects.create(
        placa="ABC-1234",
        modelo="Fiat Fiorino 1.4",
        capacidade_kg=650,
        disponivel=True,
    )


@pytest.mark.django_db
def test_criacao_veiculo(veiculo):
    assert veiculo.placa == "ABC-1234"
    assert str(veiculo) == "Fiat Fiorino 1.4 (ABC-1234)"


@pytest.mark.django_db
def test_alterar_status_disponibilidade(veiculo):
    veiculo_atualizado = FrotaService.definir_disponibilidade(
        veiculo_id=veiculo.id, disponivel=False
    )
    assert veiculo_atualizado.disponivel is False