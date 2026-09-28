from django.contrib import admin
from .models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = (
        "semestre",
        "horas_disponibles",
        "resultado",
        "fecha",
        "eliminado",
    )

    list_filter = ("eliminado", "semestre")

    search_fields = ("resultado",)

    readonly_fields = ("fecha", "fecha_eliminacion")