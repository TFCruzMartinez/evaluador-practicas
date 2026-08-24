from django.test import SimpleTestCase
from .services import evaluar_postulacion


class EvaluadorPostulacionTests(SimpleTestCase):

    def test_postulacion_aceptada(self):
        resultado = evaluar_postulacion(4, 20)
        self.assertEqual(
            resultado,
            "Aceptado: cumple los requisitos para postular."
        )

    def test_rechazado_por_semestre(self):
        resultado = evaluar_postulacion(3, 20)
        self.assertEqual(
            resultado,
            "Rechazado: no cumple con el semestre mínimo requerido."
        )

    def test_rechazado_por_horas(self):
        resultado = evaluar_postulacion(4, 15)
        self.assertEqual(
            resultado,
            "Rechazado: no cumple con la disponibilidad horaria requerida."
        )

    def test_dato_invalido_semestre(self):
        resultado = evaluar_postulacion(0, 20)
        self.assertEqual(
            resultado,
            "Dato inválido: revise los valores ingresados."
        )

    def test_dato_invalido_horas(self):
        resultado = evaluar_postulacion(4, -1)
        self.assertEqual(
            resultado,
            "Dato inválido: revise los valores ingresados."
        )
from rest_framework.test import APITestCase
from django.urls import reverse


class EvaluarAPITests(APITestCase):

    def setUp(self):
        self.url = reverse("evaluar_api")

    def test_api_postulacion_aceptada(self):
        datos = {
            "semestre": 4,
            "horas_disponibles": 25
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.data["resultado"],
            "Aceptado: cumple los requisitos para postular."
        )

    def test_api_rechazo_por_semestre(self):
        datos = {
            "semestre": 2,
            "horas_disponibles": 25
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("semestre mínimo", respuesta.data["resultado"])

    def test_api_rechazo_por_horas(self):
        datos = {
            "semestre": 5,
            "horas_disponibles": 10
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "disponibilidad horaria",
            respuesta.data["resultado"]
        )

    def test_api_campos_faltantes(self):
        respuesta = self.client.post(
            self.url,
            {"semestre": 4},
            format="json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(
            respuesta.data["error"],
            "Debe enviar semestre y horas_disponibles."
        )

    def test_api_valores_no_numericos(self):
        datos = {
            "semestre": "cuarto",
            "horas_disponibles": "veinte"
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(
            respuesta.data["error"],
            "Los valores deben ser numéricos."
        )