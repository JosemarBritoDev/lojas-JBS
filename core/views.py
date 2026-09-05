from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from clientes.models import Cliente
from vendas.models import Venda


@login_required
def dashboard_view(request):
    hoje = timezone.now().date()

    # Total Geral de Transações Realizadas Hoje
    vendas_hoje = Venda.objects.filter(criado_em__date=hoje)
    total_vendas_hoje = vendas_hoje.count()

    # Faturamento Hoje: Considera APENAS pagamentos liquidados (exclui Fiado)
    faturamento_hoje = (
        vendas_hoje.exclude(forma_pagamento=Venda.FormaPagamento.FIADO)
        .aggregate(total=Sum("valor_total"))["total"]
        or Decimal("0.00")
    )

    # Fiado Acumulado a Receber
    total_fiado = Venda.objects.filter(
        forma_pagamento=Venda.FormaPagamento.FIADO
    ).aggregate(total=Sum("valor_total"))["total"] or Decimal("0.00")

    total_clientes = Cliente.objects.filter(ativo=True).count()

    # Gráfico: Vendas liquidadas nos últimos 7 dias
    sete_dias_atras = hoje - timezone.timedelta(days=6)
    vendas_diarias = (
        Venda.objects.filter(criado_em__date__gte=sete_dias_atras)
        .exclude(forma_pagamento=Venda.FormaPagamento.FIADO)
        .annotate(data=TruncDate("criado_em"))
        .values("data")
        .annotate(total=Sum("valor_total"))
        .order_by("data")
    )

    dias_map = {v["data"].strftime("%d/%m"): str(v["total"]) for v in vendas_diarias}

    labels_grafico = []
    dados_grafico = []
    for i in range(6, -1, -1):
        dia_str = (hoje - timezone.timedelta(days=i)).strftime("%d/%m")
        labels_grafico.append(dia_str)
        dados_grafico.append(dias_map.get(dia_str, "0.00"))

    context = {
        "total_vendas_hoje": total_vendas_hoje,
        "faturamento_hoje": faturamento_hoje,
        "total_fiado": total_fiado,
        "total_clientes": total_clientes,
        "labels_grafico": labels_grafico,
        "dados_grafico": dados_grafico,
        "ultimas_vendas": Venda.objects.select_related("vendedor__user", "cliente")[:5],
    }
    return render(request, "dashboard.html", context)


@login_required
def dashboard_detalhes_view(request):
    """View responsável por exibir a lista detalhada conforme o card clicado."""
    tipo_filtro = request.GET.get("filtro", "vendas_hoje")
    hoje = timezone.now().date()

    titulo_pagina = ""
    vendas = None
    clientes = None

    if tipo_filtro == "vendas_hoje":
        titulo_pagina = "Relatório de Todas as Transações de Hoje"
        vendas = Venda.objects.filter(criado_em__date=hoje).select_related(
            "vendedor__user", "cliente", "operador"
        )

    elif tipo_filtro == "faturamento_hoje":
        titulo_pagina = "Relatório de Faturamento de Hoje (Vendas Liquidadas)"
        # Filtra apenas vendas de hoje EXCLUINDO o Fiado
        vendas = (
            Venda.objects.filter(criado_em__date=hoje)
            .exclude(forma_pagamento=Venda.FormaPagamento.FIADO)
            .select_related("vendedor__user", "cliente", "operador")
        )

    elif tipo_filtro == "fiado":
        titulo_pagina = "Relatório de Contas a Receber (Vendas no Fiado)"
        vendas = Venda.objects.filter(
            forma_pagamento=Venda.FormaPagamento.FIADO
        ).select_related("vendedor__user", "cliente", "operador")

    elif tipo_filtro == "clientes":
        titulo_pagina = "Lista de Clientes Cadastrados"
        clientes = Cliente.objects.filter(ativo=True)

    context = {
        "filtro": tipo_filtro,
        "titulo_pagina": titulo_pagina,
        "vendas": vendas,
        "clientes": clientes,
    }
    return render(request, "dashboard_detalhes.html", context)  