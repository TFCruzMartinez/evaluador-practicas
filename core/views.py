import json
from pathlib import Path

from django.shortcuts import render

from .services import evaluar_postulacion


RUTA_RAIZ = Path(__file__).resolve().parent.parent


def resumen(request):
    ruta_json = RUTA_RAIZ / "datos.json"

    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
    except FileNotFoundError:
        registros = []

    for registro in registros:
        registro["resultado"] = evaluar_postulacion(
            registro["semestre"],
            registro["horas_disponibles"]
        )

    return render(
        request,
        "resumen.html",
        {"registros": registros}
    )