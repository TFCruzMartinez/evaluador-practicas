def evaluar_postulacion(semestre, horas_disponibles):
    if semestre <= 0 or horas_disponibles < 0:
        return "Dato inválido: revise los valores ingresados."

    if semestre >= 4 and horas_disponibles >= 20:
        return "Aceptado: cumple los requisitos para postular."

    if semestre < 4:
        return "Rechazado: no cumple con el semestre mínimo requerido."

    return "Rechazado: no cumple con la disponibilidad horaria requerida."