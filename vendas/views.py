import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from caixa.models import Caixa
from clientes.models import Cliente
from funcionarios.models import Cargo, Funcionario
from produtos.models import Produto
from vendas.models import Venda
from vendas.services import VendaService


@login_required
def pdv_view(request):
    """Renderiza a interface do PDV se o operador tiver um caixa aberto."""
    caixa_aberto = Caixa.objects.filter(
        operador=request.user, status=Caixa.StatusCaixa.ABERTO
    ).first()

    produtos = Produto.objects.filter(ativo=True, quantidade_estoque__gt=0)

    # Garante que todo usuário da equipe/admin tenha um Funcionario correspondente
    for user in User.objects.filter(is_active=True):
        if not hasattr(user, "funcionario"):
            cargo_padrao, _ = Cargo.objects.get_or_create(nome="Vendedor / Balcão")
            Funcionario.objects.create(
                user=user,
                cargo=cargo_padrao,
                cpf=f"000.000.000-0{user.id}",
                comissao_percentual=Decimal("5.00"),
            )

    vendedores = Funcionario.objects.filter(ativo=True)
    clientes = Cliente.objects.filter(ativo=True)

    context = {
        "caixa": caixa_aberto,
        "produtos": produtos,
        "vendedores": vendedores,
        "clientes": clientes,
        "formas_pagamento": Venda.FormaPagamento.choices,
    }
    return render(request, "vendas/pdv.html", context)


@login_required
@require_POST
def processar_venda_api(request):
    """Endpoint AJAX/Fetch para finalizar a venda no PDV."""
    try:
        data = json.loads(request.body)
        caixa = Caixa.objects.get(id=data["caixa_id"], status=Caixa.StatusCaixa.ABERTO)
        vendedor = Funcionario.objects.get(id=data["vendedor_id"])
        cliente_id = data.get("cliente_id")

        venda = VendaService.realizar_venda(
            operador=request.user,
            vendedor=vendedor,
            caixa=caixa,
            itens_data=data["itens"],
            forma_pagamento=data["forma_pagamento"],
            cliente_id=cliente_id,
        )

        return JsonResponse(
            {
                "success": True,
                "venda_id": venda.id,
                "valor_total": str(venda.valor_total),
                "message": "Venda realizada com sucesso!",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)