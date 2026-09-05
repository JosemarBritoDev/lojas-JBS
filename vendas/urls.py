from django.urls import path
from vendas.views import pdv_view, processar_venda_api

urlpatterns = [
    path("pdv/", pdv_view, name="pdv"),
    path("api/processar/", processar_venda_api, name="venda_processar_api"),
]