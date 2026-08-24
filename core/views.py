from django.shortcuts import render
from pathlib import Path
import json
import sys


RUTA_RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(RUTA_RAIZ))

from .services import evaluar_postulacion


def resumen(request):
    ruta_json = RUTA_RAIZ / "datos.json"

    with open(ruta_json, "r", encoding="utf-8") as archivo:
        registros = json.load(archivo)

    for registro in registros:
        registro["resultado"] = evaluar_postulacion(
            registro["semestre"],
            registro["horas_disponibles"]
        )

    return render(request, "resumen.html", {"registros": registros})