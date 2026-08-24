from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiExample

from .services import evaluar_postulacion


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "semestre": {
                    "type": "integer",
                    "example": 4
                },
                "horas_disponibles": {
                    "type": "integer",
                    "example": 25
                }
            },
            "required": [
                "semestre",
                "horas_disponibles"
            ]
        }
    },
    responses={
        200: {
            "type": "object",
            "properties": {
                "semestre": {
                    "type": "integer"
                },
                "horas_disponibles": {
                    "type": "integer"
                },
                "resultado": {
                    "type": "string"
                }
            }
        }
    },
    examples=[
        OpenApiExample(
            "Postulación aceptada",
            value={
                "semestre": 4,
                "horas_disponibles": 25
            },
            request_only=True
        )
    ]
)
@api_view(["POST"])
def evaluar_api(request):
    semestre = request.data.get("semestre")
    horas_disponibles = request.data.get("horas_disponibles")

    if semestre is None or horas_disponibles is None:
        return Response(
            {
                "error": "Debe enviar semestre y horas_disponibles."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        semestre = int(semestre)
        horas_disponibles = int(horas_disponibles)

    except (TypeError, ValueError):
        return Response(
            {
                "error": "Los valores deben ser numéricos."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    resultado = evaluar_postulacion(
        semestre,
        horas_disponibles
    )

    return Response(
        {
            "semestre": semestre,
            "horas_disponibles": horas_disponibles,
            "resultado": resultado
        },
        status=status.HTTP_200_OK
    )