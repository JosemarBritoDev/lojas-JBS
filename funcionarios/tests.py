import pytest
from django.contrib.auth.models import Group, User
from funcionarios.models import Cargo, Funcionario


@pytest.mark.django_db
def test_criacao_cargo_e_funcionario():
    grupo = Group.objects.create(name="Grupo_Vendedor")
    cargo = Cargo.objects.create(nome="Vendedor 1", grupo_django=grupo)
    user = User.objects.create_user(username="joao", password="123")

    funcionario = Funcionario.objects.create(
        user=user, cargo=cargo, cpf="123.456.789-00"
    )

    assert funcionario.cargo.nome == "Vendedor 1"
    assert funcionario.user.username == "joao"
    assert str(funcionario) == "joao - Vendedor 1"