# Evaluador de Prácticas

## Propósito

El sistema Evaluador de Prácticas permite determinar si un estudiante cumple con los requisitos mínimos para postular a una práctica profesional.

La evaluación se realiza considerando:

- Semestre que cursa el estudiante.
- Horas disponibles por semana.

## Requisitos funcionales

### RF-01 - Evaluar una postulación

El sistema debe permitir evaluar una postulación utilizando el semestre y las horas disponibles del estudiante.

### RF-02 - Postulación aceptada

El sistema debe aceptar una postulación cuando:

- El estudiante cursa cuarto semestre o superior.
- El estudiante dispone de al menos 20 horas semanales.

Resultado esperado:

`Aceptado: cumple los requisitos para postular.`

### RF-03 - Rechazo por semestre

Si el estudiante cursa un semestre inferior a 4, el sistema debe rechazar la postulación.

Resultado esperado:

`Rechazado: no cumple con el semestre mínimo requerido.`

### RF-04 - Rechazo por disponibilidad

Si el estudiante cumple con el semestre requerido pero dispone de menos de 20 horas semanales, el sistema debe rechazar la postulación.

Resultado esperado:

`Rechazado: no cumple con la disponibilidad horaria requerida.`

### RF-05 - Validación de datos

El sistema debe detectar valores inválidos.

Se consideran inválidos:

- Semestre menor o igual a 0.
- Horas disponibles menores a 0.

Resultado esperado:

`Dato inválido: revise los valores ingresados.`

## API REST

El sistema debe proporcionar un endpoint:

`POST /api/evaluar/`

### Entrada

```json
{
  "semestre": 4,
  "horas_disponibles": 25
}