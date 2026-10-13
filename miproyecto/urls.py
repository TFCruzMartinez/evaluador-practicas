
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from core import views
from core.api_views import RegistroViewSet

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


# =========================================================
# ROUTER API REST - ES3
# =========================================================

router = DefaultRouter()

router.register(
    r"registros",
    RegistroViewSet,
    basename="registro"
)


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

urlpatterns = [
    # Administrador Django
    path("admin/", admin.site.urls),

    # Autenticación web
    path("login/", views.vista_login, name="login"),
    path("logout/", views.vista_logout, name="logout"),

    # CRUD web de registros
    path("registros/", views.lista, name="lista"),

    path(
        "registros/crear/",
        views.crear,
        name="crear",
    ),

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

    # API REST mediante DefaultRouter
    path(
        "api/",
        include(router.urls),
    ),

    # Obtener token de autenticación
    path(
        "api/token/",
        obtain_auth_token,
        name="api_token",
    ),

    # Documentación OpenAPI
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Documentación Swagger
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]
