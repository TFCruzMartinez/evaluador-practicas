
# Uso de Inteligencia Artificial en el proyecto

## Proyecto: Evaluador de Prácticas

Durante el desarrollo del proyecto Evaluador de Prácticas se utilizó ChatGPT como herramienta de apoyo para analizar el código existente, orientar la implementación y revisar aspectos de persistencia, seguridad, arquitectura REST y pruebas automatizadas.

La Inteligencia Artificial se utilizó como apoyo técnico. Sus propuestas fueron revisadas y verificadas mediante herramientas de Django, pruebas automatizadas y solicitudes HTTP reales.

## 1. Análisis del proyecto existente

Se revisó la estructura original del proyecto para identificar los componentes que debían mantenerse.

Se identificaron:

- La función `evaluar_postulacion()` en `core/services.py`.
- La API original de evaluación.
- El almacenamiento inicial mediante `datos.json`.
- Las pruebas automatizadas de la lógica de evaluación.
- El sistema de autenticación y roles.

Se decidió conservar `evaluar_postulacion()` como fuente principal de la lógica de negocio para evitar duplicar las reglas de evaluación.

## 2. Migración a base de datos

Durante la EVA2 se implementó persistencia mediante Django ORM y SQLite.

Se creó el modelo `Registro`, con los siguientes campos:

- `semestre`
- `horas_disponibles`
- `resultado`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

Se generaron y aplicaron las migraciones correspondientes.

El CRUD dejó de depender de `datos.json` y comenzó a utilizar Django ORM.

## 3. CRUD

Se implementaron las operaciones:

- Crear registros.
- Listar registros.
- Editar registros.
- Eliminar registros mediante borrado lógico.

Al crear o editar un registro se utiliza `evaluar_postulacion()` para calcular automáticamente el resultado.

La lógica de evaluación permanece centralizada en `core/services.py`.

## 4. Borrado lógico

Se implementó borrado lógico mediante los campos:

- `eliminado`
- `fecha_eliminacion`

El método `soft_delete()` marca el registro como eliminado y almacena la fecha correspondiente.

El registro permanece físicamente en la base de datos, pero deja de aparecer en las consultas normales.

Los registros eliminados pueden continuar revisándose desde Django Admin.

## 5. Administración de Django

Se configuró Django Admin para facilitar la administración de registros.

Se incorporaron:

- Columnas de información relevante.
- Filtros.
- Campo de búsqueda.
- Visualización del estado de eliminación.

## 6. Autenticación y roles de la aplicación web

Se implementó autenticación mediante el sistema de usuarios de Django.

Se definieron tres roles utilizando Groups:

### viewer

Puede consultar registros, pero no crear, editar ni eliminar.

### normal

Puede consultar y crear registros, pero no editar ni eliminar.

### admin

Puede consultar, crear, editar y eliminar registros mediante borrado lógico.

Los permisos se comprueban desde el servidor y no dependen únicamente de ocultar opciones de la interfaz.

## 7. Seguridad de la aplicación web

Los formularios POST mantienen la protección CSRF de Django mediante:

`{% csrf_token %}`

Se utilizan mecanismos de autenticación y autorización de Django.

Las pruebas de permisos verificaron respuestas HTTP 403 cuando usuarios autenticados intentaron acceder a operaciones restringidas.

## 8. Pruebas automatizadas de la EVA2

Durante la EVA2 se implementaron 20 pruebas automatizadas.

Estas verificaban:

- Lógica de evaluación.
- API original.
- Modelo `Registro`.
- Borrado lógico.
- Autenticación web.
- Roles `viewer`, `normal` y `admin`.
- Edición y recálculo del resultado.

El resultado de la EVA2 fue:

- 20 pruebas ejecutadas.
- 20 pruebas aprobadas.
- Estado: `OK`.

## 9. Uso de Inteligencia Artificial en la EVA2

### Herramienta utilizada

ChatGPT.

### Consulta realizada

"¿Cómo puedo migrar el Evaluador de Prácticas desde datos.json a SQLite utilizando un modelo de Django, migraciones y roles de usuario, sin modificar la función original evaluar_postulacion?"

### Decisiones adoptadas

Se conservó la función `evaluar_postulacion()` como única fuente de las reglas de evaluación.

Se revisó la implementación del modelo, las migraciones y los permisos.

También se verificó que las restricciones de acceso fueran aplicadas desde el servidor.

## 10. Evolución del proyecto para la ES3

En la ES3 se amplió el proyecto para implementar una API REST basada en recursos mediante Django REST Framework.

La API anterior utilizaba el endpoint:

`POST /api/evaluar/`

La nueva implementación utiliza el recurso:

`/api/registros/`

Este cambio permite gestionar registros mediante los métodos HTTP correspondientes.

### Endpoints implementados

| Método | Endpoint | Función |
|---|---|---|
| GET | /api/registros/ | Listar registros |
| POST | /api/registros/ | Crear registro |
| GET | /api/registros/{id}/ | Consultar registro |
| PUT | /api/registros/{id}/ | Actualizar registro |
| PATCH | /api/registros/{id}/ | Actualizar parcialmente |
| DELETE | /api/registros/{id}/ | Realizar borrado lógico |

Las rutas se generan mediante `DefaultRouter`.

## 11. Serialización y validación

Se creó `core/serializers.py` utilizando `ModelSerializer`.

El serializer define explícitamente los campos del modelo `Registro`.

Los siguientes campos se configuraron como de solo lectura:

- `id`
- `resultado`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

Esto impide que el cliente modifique directamente valores que deben ser controlados por el servidor.

También se incorporaron validaciones:

- `semestre` debe ser mayor que cero.
- `horas_disponibles` no puede ser negativo.
- Ambos campos deben contener números enteros.
- Los campos obligatorios deben estar presentes.

Los métodos `create()` y `update()` utilizan `evaluar_postulacion()` para calcular el resultado.

## 12. ModelViewSet y DefaultRouter

Se implementó `RegistroViewSet` en `core/api_views.py`.

La clase hereda de `ModelViewSet`, proporcionando operaciones REST para el recurso `Registro`.

Se utilizó `DefaultRouter` en `miproyecto/urls.py` para registrar las rutas automáticamente.

El ViewSet consulta únicamente registros con:

`eliminado=False`

La operación DELETE utiliza `perform_destroy()` para ejecutar `soft_delete()`.

## 13. Autenticación por token

Se configuró Django REST Framework para utilizar:

- `TokenAuthentication`
- `SessionAuthentication`

También se estableció `IsAuthenticated` como permiso global predeterminado.

Se habilitó el endpoint:

`POST /api/token/`

Este permite obtener un token mediante credenciales válidas.

Para las pruebas locales se generaron tokens para los usuarios:

- `viewer_api`
- `normal_api`
- `admin_api`

Los valores de los tokens no se incorporaron a las evidencias.

La autenticación por token debe utilizarse mediante HTTPS en un entorno de producción.

## 14. Autorización diferenciada en la API

Se creó una clase de permisos personalizada llamada `RegistroPermission`.

Esta reutiliza los roles existentes del proyecto.

### Permisos por rol

| Operación | viewer | normal | admin |
|---|---|---|---|
| Consultar | Sí | Sí | Sí |
| Crear | No | Sí | Sí |
| Editar | No | No | Sí |
| Eliminar | No | No | Sí |

La API exige autenticación antes de autorizar las operaciones.

Un usuario autenticado que no posee los permisos necesarios recibe una respuesta HTTP 403.

Una solicitud sin credenciales recibe una respuesta HTTP 401.

## 15. Consulta a la IA sobre seguridad en la ES3

### Herramienta

ChatGPT.

### Problema planteado

Se necesitaba proteger la nueva API REST sin perder los roles implementados durante la EVA2.

### Consulta realizada

"¿Cómo puedo implementar autenticación por token y permisos diferenciados en Django REST Framework utilizando ModelViewSet, DefaultRouter y los grupos viewer, normal y admin, conservando las reglas de acceso existentes y evitando que usuarios no autorizados modifiquen registros?"

### Propuesta de la IA

La propuesta inicial utilizaba `IsAuthenticated` y `IsAdminUser` para permitir consultas a usuarios autenticados y modificaciones a usuarios administrativos.

### Revisión y corrección

Durante la revisión se identificó que esta propuesta no respetaba completamente los roles originales del proyecto.

En particular, el rol `normal` debía poder crear registros, pero no editarlos ni eliminarlos.

También se identificó que pertenecer al grupo `admin` no equivale automáticamente a tener `is_staff=True`.

Por este motivo, se reemplazó la propuesta inicial por una clase `RegistroPermission` que reutiliza las funciones de roles de la aplicación.

### Decisión final

Se mantuvo la lógica de autorización de la EVA2 y se adaptó a los métodos HTTP de la API REST.

La decisión fue verificada mediante pruebas automatizadas y solicitudes HTTP reales.

Este proceso demuestra que las respuestas de la IA fueron revisadas críticamente y corregidas cuando no cumplían los requisitos del proyecto.

## 16. Pruebas automatizadas de la ES3

Se actualizaron las cinco pruebas correspondientes a la API original.

También se incorporaron 13 pruebas nuevas de seguridad y funcionamiento REST.

Las pruebas verifican:

- Acceso sin autenticación.
- Acceso mediante token válido.
- Rechazo de token inválido.
- Consulta de registros por viewer.
- Restricción de creación para viewer.
- Creación por normal.
- Restricción de edición para normal.
- Edición por admin.
- Borrado lógico por admin.
- Protección de campos de solo lectura.
- Validación de semestre.
- Validación de horas disponibles.
- Respuesta 404 para registros inexistentes.

Se ejecutó:

`python manage.py test`

Resultado:

- 33 pruebas ejecutadas.
- 33 pruebas aprobadas.
- Resultado: `OK`.

La salida de las pruebas se guardó en:

`pruebas/01_tests.txt`

## 17. Evidencias de solicitudes HTTP

Se realizaron pruebas manuales utilizando `curl` y el servidor de desarrollo Django.

Los resultados se almacenaron en la carpeta `pruebas/`.

| Archivo | Prueba | Resultado |
|---|---|---|
| 02_sin_autenticacion.txt | GET sin token | 401 |
| 03_viewer_consulta.txt | GET con viewer | 200 |
| 04_viewer_sin_permiso.txt | POST con viewer | 403 |
| 05_normal_crear.txt | POST con normal | 201 |
| 06_normal_sin_permiso_editar.txt | PATCH con normal | 403 |
| 07_admin_editar.txt | PATCH con admin | 200 |
| 08_admin_eliminar.txt | DELETE con admin | 204 |
| 09_verificar_borrado_logico.txt | Consulta de base de datos | Eliminado=True |
| 10_registro_eliminado_404.txt | GET de registro eliminado | 404 |
| 11_validacion_datos_invalidos.txt | POST con valores inválidos | 400 |
| 12_campos_obligatorios.txt | POST con campo faltante | 400 |
| 13_valores_no_numericos.txt | POST con texto en campos numéricos | 400 |

Estas evidencias permiten comprobar el funcionamiento de la API, la autenticación, la autorización y el manejo de errores.

## 18. Validación de las propuestas de IA

Las propuestas de Inteligencia Artificial no se incorporaron sin revisión.

Se utilizaron los siguientes mecanismos de validación:

- `python manage.py check`
- Migraciones de Django.
- `python manage.py test`
- Pruebas HTTP con `curl`.
- Verificación de permisos por rol.
- Revisión de respuestas JSON.
- Consulta directa del estado de borrado lógico en SQLite.

Durante la adaptación de la API, cinco pruebas originales fallaron porque utilizaban la ruta anterior `evaluar_api`.

Estas pruebas fueron actualizadas para utilizar las nuevas rutas REST, autenticación y códigos HTTP.

Después de las correcciones, el proyecto completó satisfactoriamente las 33 pruebas automatizadas.

## 19. Resultado final

El uso de Inteligencia Artificial permitió apoyar el desarrollo de la EVA2 y su evolución hacia la ES3.

El proyecto conserva su lógica original de evaluación y ahora incorpora:

- Persistencia mediante Django ORM y SQLite.
- CRUD de registros.
- Borrado lógico.
- Autenticación y roles en la aplicación web.
- API REST mediante Django REST Framework.
- ModelSerializer con validaciones.
- ModelViewSet y DefaultRouter.
- Autenticación por token.
- Permisos diferenciados por rol.
- Respuestas HTTP y errores JSON.
- Documentación OpenAPI y Swagger.
- 33 pruebas automatizadas aprobadas.
- Evidencias de ejecución manual.

La IA actuó como herramienta de apoyo. Las decisiones finales fueron revisadas y comprobadas mediante pruebas, manteniendo la coherencia con los requisitos y el funcionamiento original del proyecto.
