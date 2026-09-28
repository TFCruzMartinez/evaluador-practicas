from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Registro
from .services import evaluar_postulacion


# ==========================================================
# PRUEBAS DE LA LÓGICA ORIGINAL
# ==========================================================

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
        resultado = evaluar_postulacion(4, 19)
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


# ==========================================================
# PRUEBAS DE LA API
# ==========================================================

class EvaluarAPITests(APITestCase):

    def setUp(self):
        self.url = reverse("evaluar_api")

    def test_api_postulacion_aceptada(self):
        datos = {
            "semestre": 4,
            "horas_disponibles": 20
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "Aceptado",
            respuesta.data["resultado"]
        )

    def test_api_rechazado_por_semestre(self):
        datos = {
            "semestre": 3,
            "horas_disponibles": 20
        }

        respuesta = self.client.post(
            self.url,
            datos,
            format="json"
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(
            "semestre mínimo",
            respuesta.data["resultado"]
        )

    def test_api_rechazado_por_horas(self):
        datos = {
            "semestre": 4,
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


# ==========================================================
# PRUEBAS DEL MODELO
# ==========================================================

class RegistroModelTests(TestCase):

    def test_crear_registro(self):
        registro = Registro.objects.create(
            semestre=4,
            horas_disponibles=25,
            resultado=evaluar_postulacion(4, 25)
        )

        self.assertEqual(registro.semestre, 4)
        self.assertEqual(registro.horas_disponibles, 25)
        self.assertFalse(registro.eliminado)
        self.assertIn("Aceptado", registro.resultado)

    def test_borrado_logico(self):
        registro = Registro.objects.create(
            semestre=4,
            horas_disponibles=25,
            resultado=evaluar_postulacion(4, 25)
        )

        registro.soft_delete()
        registro.refresh_from_db()

        self.assertTrue(registro.eliminado)
        self.assertIsNotNone(registro.fecha_eliminacion)

        # El registro continúa físicamente en la BD
        self.assertTrue(
            Registro.objects.filter(pk=registro.pk).exists()
        )


# ==========================================================
# PRUEBAS DE AUTENTICACIÓN Y ROLES
# ==========================================================

class PermisosTests(TestCase):

    def setUp(self):
        self.viewer_group = Group.objects.create(name="viewer")
        self.normal_group = Group.objects.create(name="normal")
        self.admin_group = Group.objects.create(name="admin")

        self.viewer = User.objects.create_user(
            username="lector_test",
            password="ClaveTest123!"
        )
        self.viewer.groups.add(self.viewer_group)

        self.normal = User.objects.create_user(
            username="operador_test",
            password="ClaveTest123!"
        )
        self.normal.groups.add(self.normal_group)

        self.admin_user = User.objects.create_user(
            username="admin_test",
            password="ClaveTest123!"
        )
        self.admin_user.groups.add(self.admin_group)

        self.registro = Registro.objects.create(
            semestre=4,
            horas_disponibles=25,
            resultado=evaluar_postulacion(4, 25)
        )

    def test_usuario_no_autenticado_va_a_login(self):
        respuesta = self.client.get(reverse("lista"))

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/login/", respuesta.url)

    def test_viewer_puede_ver_lista(self):
        self.client.login(
            username="lector_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.get(reverse("lista"))

        self.assertEqual(respuesta.status_code, 200)

    def test_viewer_no_puede_crear(self):
        self.client.login(
            username="lector_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.get(reverse("crear"))

        self.assertEqual(respuesta.status_code, 403)

    def test_normal_puede_crear(self):
        self.client.login(
            username="operador_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.post(
            reverse("crear"),
            {
                "semestre": 4,
                "horas_disponibles": 25
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertTrue(
            Registro.objects.filter(
                semestre=4,
                horas_disponibles=25,
                eliminado=False
            ).exists()
        )

    def test_normal_no_puede_editar(self):
        self.client.login(
            username="operador_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.get(
            reverse(
                "editar",
                args=[self.registro.pk]
            )
        )

        self.assertEqual(respuesta.status_code, 403)

    def test_normal_no_puede_eliminar(self):
        self.client.login(
            username="operador_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.get(
            reverse(
                "eliminar",
                args=[self.registro.pk]
            )
        )

        self.assertEqual(respuesta.status_code, 403)

    def test_admin_puede_editar_y_recalcula_resultado(self):
        self.client.login(
            username="admin_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.post(
            reverse(
                "editar",
                args=[self.registro.pk]
            ),
            {
                "semestre": 3,
                "horas_disponibles": 25
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        self.registro.refresh_from_db()

        self.assertEqual(self.registro.semestre, 3)
        self.assertEqual(
            self.registro.resultado,
            "Rechazado: no cumple con el semestre mínimo requerido."
        )

    def test_admin_puede_eliminar_logicamente(self):
        self.client.login(
            username="admin_test",
            password="ClaveTest123!"
        )

        respuesta = self.client.post(
            reverse(
                "eliminar",
                args=[self.registro.pk]
            )
        )

        self.assertEqual(respuesta.status_code, 302)

        self.registro.refresh_from_db()

        self.assertTrue(self.registro.eliminado)
        self.assertIsNotNone(
            self.registro.fecha_eliminacion
        )
