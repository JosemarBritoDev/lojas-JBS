from django.contrib import admin
from django.urls import include, path
from core.views import dashboard_detalhes_view, dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/detalhes/", dashboard_detalhes_view, name="dashboard_detalhes"),
    path("vendas/", include("vendas.urls")),
]