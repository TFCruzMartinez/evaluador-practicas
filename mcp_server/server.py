import requests
from mcp.server import MCPServer


mcp = MCPServer("Evaluador de Practicas")

API_URL = "https://evaluador-practicas.onrender.com/api/evaluar/"


@mcp.tool()
def evaluar_postulacion(
    semestre: int,
    horas_disponibles: int
) -> str:
    """Evalua si un estudiante cumple los requisitos para una practica."""

    payload = {
        "semestre": semestre,
        "horas_disponibles": horas_disponibles,
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return (
            f"Semestre: {data['semestre']}\n"
            f"Horas disponibles: {data['horas_disponibles']}\n"
            f"Resultado: {data['resultado']}"
        )

    except requests.RequestException as error:
        return f"Error al consumir la API: {error}"
