# Plan de Migración y Mejora
## Proyecto: Evaluador de Prácticas

## 1. Objetivo

Actualizar el proyecto Evaluador de Prácticas manteniendo la lógica de negocio original e incorporando persistencia mediante base de datos, administración de registros, operaciones CRUD, autenticación, autorización por roles, seguridad y pruebas automatizadas.

La función `evaluar_postulacion()` se mantiene como fuente principal de las reglas de evaluación.

---

## 2. Estado inicial

El proyecto inicialmente contaba con:

- Aplicación desarrollada con Django.
- Función `evaluar_postulacion()` en `core/services.py`.
- Almacenamiento de registros mediante `datos.json`.
- API para evaluar postulaciones.
- Documentación OpenAPI/Swagger.
- Pruebas automatizadas para la lógica de evaluación y la API.

La principal mejora requerida fue migrar la gestión de registros desde el archivo JSON hacia una base de datos administrada mediante Django ORM.

---

## 3. Etapa 1: Persistencia de datos

### Objetivo

Reemplazar el uso de `datos.json` en el CRUD por persistencia mediante SQLite y Django ORM.

### Implementación

Se creó el modelo `Registro` con los siguientes campos:

- `semestre`
- `horas_disponibles`
- `resultado`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

Se generaron y aplicaron las migraciones de Django.

### Validación

Se utilizaron los comandos:

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py makemigrations --check --dry-run`

El sistema confirmó que las migraciones fueron aplicadas y que no existían cambios pendientes.

---

## 4. Etapa 2: Django Admin

### Objetivo

Permitir la administración de los registros desde el panel administrativo de Django.

### Implementación

Se registró el modelo `Registro` en `core/admin.py`.

Se configuraron:

- Columnas de información.
- Filtros por estado de eliminación y semestre.
- Búsqueda.
- Campos de fecha de solo lectura.

### Validación

Se verificó desde Django Admin que los registros fueran visibles y que los filtros y búsqueda estuvieran disponibles.

---

## 5. Etapa 3: CRUD

### Objetivo

Implementar las operaciones necesarias para administrar los registros.

### Funcionalidades

Se implementaron:

- CREATE: creación de registros.
- READ: listado de registros activos.
- UPDATE: modificación de registros.
- DELETE: eliminación lógica.

Las vistas trabajan mediante Django ORM y dejaron de depender de `datos.json`.

### Reutilización de lógica

La creación y edición reutilizan:

`evaluar_postulacion()`

ubicada en:

`core/services.py`

De esta forma, no se duplicaron las reglas de evaluación.

---

## 6. Etapa 4: Borrado lógico

### Objetivo

Evitar la eliminación física de información.

### Implementación

Se incorporaron al modelo:

- `eliminado`
- `fecha_eliminacion`

El método `soft_delete()` marca un registro como eliminado y almacena la fecha correspondiente.

El listado principal utiliza únicamente registros donde:

`eliminado=False`

### Validación

Se comprobó que un registro eliminado desaparece del listado de la aplicación, pero continúa almacenado y visible desde Django Admin.

---

## 7. Etapa 5: Autenticación

### Objetivo

Restringir el acceso al sistema a usuarios autenticados.

### Implementación

Se utilizaron las herramientas de autenticación de Django para:

- Inicio de sesión.
- Cierre de sesión.
- Protección de vistas mediante `login_required`.

Un usuario que no ha iniciado sesión es redirigido al formulario de acceso.

---

## 8. Etapa 6: Roles y autorización

### Objetivo

Aplicar diferentes niveles de acceso según el tipo de usuario.

Se utilizaron Django Groups.

### Rol viewer

Permisos:

- Consultar registros.

Restricciones:

- No puede crear.
- No puede editar.
- No puede eliminar.

### Rol normal

Permisos:

- Consultar registros.
- Crear registros.

Restricciones:

- No puede editar.
- No puede eliminar.

### Rol admin

Permisos:

- Consultar.
- Crear.
- Editar.
- Eliminar lógicamente.

Los superusuarios también tienen acceso administrativo completo.

### Validación

Se realizaron pruebas manuales con usuarios asociados a los distintos grupos.

También se intentó acceder directamente a URL restringidas.

Los accesos no autorizados devolvieron:

`HTTP 403 Forbidden`

Esto permite comprobar que la autorización se realiza en el servidor y no solamente ocultando opciones en la interfaz.

---

## 9. Etapa 7: Seguridad

Se mantuvo activa la protección CSRF de Django.

Los formularios POST incluyen:

`{% csrf_token %}`

No se utilizaron mecanismos para desactivar la protección CSRF.

También se mantuvieron los mecanismos de autenticación y sesiones proporcionados por Django.

---

## 10. Etapa 8: Pruebas automatizadas

### Objetivo

Comprobar que las funcionalidades originales y las nuevas características funcionen correctamente.

Se conservaron pruebas para:

- Lógica de evaluación.
- API.

Se incorporaron pruebas para:

- Modelo `Registro`.
- Creación de registros.
- Borrado lógico.
- Autenticación.
- Rol `viewer`.
- Rol `normal`.
- Rol `admin`.
- Restricciones de acceso.
- Edición de registros.
- Recálculo automático del resultado.
- Eliminación lógica.

### Resultado

Se ejecutó:

`python manage.py test`

## 11.1 Actualización de prioridades MoSCoW

Durante la migración se actualizó la priorización de los requisitos del proyecto de acuerdo con el alcance real de esta entrega.

### Must have

- Persistencia mediante SQLite y Django ORM.
- Modelo `Registro` y migraciones de Django.
- CRUD de registros.
- Reutilización de la función original `evaluar_postulacion`.
- Borrado lógico de registros.
- Autenticación mediante login y logout.
- Autorización mediante los roles `admin`, `normal` y `viewer`.
- Protección CSRF en formularios.
- Validación de permisos desde el servidor.}

La autenticación, que anteriormente no formaba parte del alcance principal, pasó a ser un requisito **Must**, debido a que es necesaria para implementar correctamente el control de acceso por roles.

### Should have

- Administración de registros mediante Django Admin.
- Búsqueda y filtros desde el panel de administración.
- Pruebas automatizadas para permisos, modelo y CRUD.

### Could have

- Mejoras adicionales en la interfaz visual.
- Nuevas funcionalidades para la API.

### Won't have en esta entrega

- Automatización de procesos externos.
- Funcionalidades adicionales que no formen parte de la migración solicitada.
La autenticación, que anteriormente no formaba parte del alcance principal, pasó a ser un requisito **Must**, debido a que es necesaria para implementar correctamente el control de acceso por roles.

### Should have

- Administración de registros mediante Django Admin.
- Búsqueda y filtros desde el panel de administración.
- Pruebas automatizadas para permisos, modelo y CRUD.

### Could have

- Mejoras adicionales en la interfaz visual.
- Nuevas funcionalidades para la API.

### Won't have en esta entrega

- Automatización de procesos externos.
- Funcionalidades adicionales que no formen parte de la migración solicitada.
Resultado final:

- 20 tests ejecutados.
- 20 tests aprobados.
- Estado: `OK`.

---

## 11. Compatibilidad

Durante la migración se mantuvieron los componentes existentes que continúan siendo utilizados por el proyecto:

- API de evaluación.
- Swagger/OpenAPI.
- Función `evaluar_postulacion()`.
- Configuración principal de Django.

El cambio principal consistió en reemplazar el uso de JSON para el CRUD por persistencia mediante Django ORM.

---

## 12. Resultado final

El proyecto quedó actualizado con:

- Persistencia mediante SQLite.
- Modelo administrado con Django ORM.
- Django Admin.
- CRUD completo.
- Borrado lógico.
- Autenticación.
- Roles `viewer`, `normal` y `admin`.
- Autorización aplicada en el servidor.
- Protección CSRF.
- Reutilización de la lógica original.
- API existente conservada.
- Pruebas automatizadas.
- Documentación del proceso de migración.

La implementación fue validada mediante pruebas manuales y automatizadas antes de considerar finalizada la migración.
