
# Evaluador de Prácticas

Proyecto académico desarrollado con Python, Django y Django REST Framework.

El sistema permite evaluar postulaciones a prácticas profesionales según el semestre cursado y las horas disponibles.

## 1. Funcionalidades

- Evaluación automática de postulaciones.
- Persistencia de datos mediante SQLite.
- Administración de registros con Django ORM.
- CRUD mediante aplicación web y API REST.
- Borrado lógico.
- Autenticación de usuarios.
- Autenticación por token en la API.
- Permisos diferenciados por roles.
- Validación de datos mediante serializers.
- Documentación Swagger/OpenAPI.
- Pruebas automatizadas.

## 2. Tecnologías utilizadas

- Python 3
- Django 4.2
- Django REST Framework
- SQLite
- drf-spectacular
- Git y GitHub

## 3. Instalación

Clonar el repositorio:

    git clone https://github.com/TFCruzMartinez/evaluador-practicas.git

Ingresar a la carpeta:

    cd evaluador-practicas

Crear el entorno virtual:

    python3 -m venv .venv

Activarlo en macOS o Linux:

    source .venv/bin/activate

Instalar las dependencias:

    pip install -r requirements.txt

Aplicar las migraciones:

    python manage.py migrate

Iniciar el servidor:

    python manage.py runserver

La aplicación estará disponible en:

http://127.0.0.1:8000/

## 4. Reglas de evaluación

La función principal se encuentra en:

`core/services.py`

La postulación es aceptada cuando:

- El semestre es igual o superior a 4.
- Las horas disponibles son iguales o superiores a 20.

Si no se cumplen estas condiciones, el sistema informa el motivo del rechazo.

## 5. Modelo de datos

El modelo `Registro` incluye:

- `id`
- `semestre`
- `horas_disponibles`
- `resultado`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

El campo `resultado` se calcula automáticamente.

## 6. API REST

La API utiliza Django REST Framework, ModelViewSet y DefaultRouter.

### Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /api/registros/ | Listar registros |
| POST | /api/registros/ | Crear registro |
| GET | /api/registros/{id}/ | Consultar registro |
| PUT | /api/registros/{id}/ | Actualizar registro |
| PATCH | /api/registros/{id}/ | Actualizar parcialmente |
| DELETE | /api/registros/{id}/ | Borrado lógico |
| POST | /api/token/ | Obtener token |

Los registros eliminados no aparecen en las consultas normales de la API.

## 7. Autenticación

La API utiliza autenticación por token y sesión.

Para obtener un token, se debe enviar una solicitud POST a:

`/api/token/`

Con credenciales válidas:

    {
      "username": "usuario",
      "password": "contraseña"
    }

Para utilizar el token en una solicitud HTTP:

    Authorization: Token TU_TOKEN

Los tokens son credenciales privadas y no deben publicarse.

En producción se debe utilizar HTTPS.

## 8. Roles y permisos

El proyecto utiliza tres grupos de usuarios.

| Operación | viewer | normal | admin |
|---|---|---|---|
| Consultar | Sí | Sí | Sí |
| Crear | No | Sí | Sí |
| Editar | No | No | Sí |
| Eliminar | No | No | Sí |

Los permisos son verificados desde el servidor.

Para utilizar los endpoints protegidos se requiere un usuario autenticado y perteneciente a un grupo autorizado.

## 9. Validaciones

El serializer valida que:

- El semestre sea mayor que cero.
- Las horas disponibles no sean negativas.
- Los valores sean números enteros.
- Se proporcionen los campos obligatorios.

Los campos de resultado, fecha y eliminación son de solo lectura.

## 10. Respuestas HTTP

La API utiliza códigos HTTP para informar el resultado de las solicitudes.

| Código | Significado |
|---|---|
| 200 | Consulta o actualización exitosa |
| 201 | Registro creado |
| 204 | Eliminación lógica realizada |
| 400 | Datos inválidos |
| 401 | Credenciales ausentes o inválidas |
| 403 | Usuario sin permisos |
| 404 | Registro inexistente o eliminado |

## 11. Documentación de la API

Esquema OpenAPI:

http://127.0.0.1:8000/api/schema/

Interfaz Swagger:

http://127.0.0.1:8000/api/docs/

## 12. Pruebas automatizadas

Ejecutar:

    python manage.py test

Resultado verificado durante el desarrollo de la ES3:

- 33 pruebas ejecutadas.
- 33 pruebas aprobadas.
- Estado: OK.

Las pruebas comprueban la lógica de negocio, el modelo, la API REST, la autenticación, los permisos, las validaciones y el borrado lógico.

## 13. Evidencias

La carpeta `pruebas/` contiene los resultados de las pruebas automatizadas y las solicitudes HTTP realizadas durante la ES3.

Incluye evidencias de:

- Autenticación requerida.
- Acceso mediante token.
- Permisos por rol.
- Creación y edición de registros.
- Borrado lógico.
- Respuestas HTTP 400, 401, 403 y 404.
- Validación de campos obligatorios y tipos de datos.

Las evidencias no deben contener tokens ni contraseñas.

## 14. Uso de Inteligencia Artificial

El archivo `ia.md` documenta cómo se utilizó ChatGPT como herramienta de apoyo durante el desarrollo.

Incluye:

- Consultas realizadas.
- Propuestas de implementación.
- Revisión de decisiones de seguridad.
- Correcciones efectuadas.
- Verificación mediante pruebas.

## 15. Consideraciones de seguridad

- Mantener la clave secreta de Django fuera del repositorio en producción.
- No publicar tokens ni contraseñas.
- Utilizar HTTPS en producción.
- Configurar correctamente DEBUG y ALLOWED_HOSTS.
- Aplicar autenticación y autorización desde el servidor.

## 16. Autoría

Proyecto académico: Evaluador de Prácticas.

Carrera: Analista Programador.

Institución: INACAP.
