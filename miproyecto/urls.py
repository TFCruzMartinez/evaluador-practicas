from django.contrib import admin
from django.urls import path

from core.views import resumen
from core.api_views import evaluar_api

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("resumen/", resumen, name="resumen"),

    # API
    path("api/evaluar/", evaluar_api, name="evaluar_api"),

    # OpenAPI / Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]