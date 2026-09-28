from django.contrib import admin
from django.urls import path

from core import views
from core.api_views import evaluar_api

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # Administrador
    path("admin/", admin.site.urls),

    # Autenticación
    path("login/", views.vista_login, name="login"),
    path("logout/", views.vista_logout, name="logout"),

    # CRUD de registros
    path("registros/", views.lista, name="lista"),
    path("registros/crear/", views.crear, name="crear"),
    path(
        "registros/<int:pk>/editar/",
        views.editar,
        name="editar",
    ),
    path(
        "registros/<int:pk>/eliminar/",
        views.eliminar,
        name="eliminar",
    ),

    # API
    path("api/evaluar/", evaluar_api, name="evaluar_api"),

    # OpenAPI / Swagger
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]