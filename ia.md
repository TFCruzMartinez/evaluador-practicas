# Uso de Inteligencia Artificial en el proyecto

## Proyecto: Evaluador de Prácticas

Durante el desarrollo y mejora del proyecto Evaluador de Prácticas se utilizó Inteligencia Artificial como herramienta de apoyo para analizar el código existente, orientar la migración del sistema y proponer mejoras de seguridad, persistencia de datos y pruebas.

La IA fue utilizada como apoyo durante el proceso de desarrollo. Las propuestas generadas fueron revisadas y posteriormente verificadas mediante pruebas manuales y automáticas.

## 1. Análisis del proyecto existente

Se revisó la estructura original del proyecto para identificar su funcionamiento y los componentes que debían mantenerse.

Se identificaron principalmente:

- La función `evaluar_postulacion()` ubicada en `core/services.py`.
- La API existente para evaluar postulaciones.
- El almacenamiento inicial de información mediante `datos.json`.
- Las pruebas automatizadas existentes para la lógica de evaluación y la API.

Se decidió conservar la función `evaluar_postulacion()` como fuente principal de la lógica de negocio para evitar duplicar las reglas de evaluación.

## 2. Migración a base de datos

La IA fue utilizada como apoyo para implementar la persistencia de información mediante Django ORM y SQLite.

Se creó el modelo `Registro`, que almacena:

- Semestre.
- Horas disponibles.
- Resultado de la evaluación.
- Fecha de creación.
- Estado de eliminación.
- Fecha de eliminación.

Después de crear el modelo se generaron y aplicaron las migraciones correspondientes.

El CRUD dejó de depender de `datos.json` y comenzó a trabajar con la base de datos mediante Django ORM.

## 3. CRUD

Se implementaron las operaciones principales del sistema:

- Crear registros.
- Listar registros.
- Editar registros.
- Eliminar registros mediante borrado lógico.

Al crear o editar un registro se reutiliza la función `evaluar_postulacion()` para calcular el resultado.

De esta forma, las reglas de evaluación permanecen centralizadas en `core/services.py`.

## 4. Borrado lógico

En lugar de eliminar físicamente los registros de la base de datos, se implementó un borrado lógico.

El modelo utiliza los campos:

- `eliminado`
- `fecha_eliminacion`

Cuando un registro es eliminado desde la aplicación, permanece almacenado en la base de datos, pero deja de aparecer en el listado principal.

Los registros eliminados pueden continuar siendo consultados desde Django Admin.

## 5. Administración de Django

Se configuró Django Admin para facilitar la administración de los registros.

Se incorporaron:

- Columnas para visualizar información relevante.
- Filtros.
- Campo de búsqueda.
- Visualización del estado de eliminación.

Esto permite administrar y revisar los registros directamente desde el panel de administración de Django.

## 6. Autenticación y autorización

Se incorporó autenticación mediante el sistema de usuarios de Django.

También se implementaron tres niveles de acceso utilizando Groups:

### viewer

Puede:

- Iniciar sesión.
- Consultar registros.

No puede crear, editar ni eliminar registros.

### normal

Puede:

- Iniciar sesión.
- Consultar registros.
- Crear registros.

No puede editar ni eliminar registros.

### admin

Puede:

- Consultar registros.
- Crear registros.
- Editar registros.
- Eliminar registros mediante borrado lógico.

Los permisos se validan en las vistas del servidor. Por lo tanto, un usuario no autorizado tampoco puede acceder a una operación restringida escribiendo manualmente su URL.

## 7. Seguridad

Los formularios que utilizan solicitudes POST mantienen la protección CSRF proporcionada por Django mediante:

`{% csrf_token %}`

También se utilizan las herramientas de autenticación y autorización proporcionadas por Django.

Durante las pruebas se verificó que los usuarios sin permisos recibieran una respuesta HTTP 403 al intentar acceder directamente a operaciones restringidas.

## 8. Pruebas

Se ampliaron las pruebas automatizadas del proyecto.

Las pruebas comprueban:

- La lógica de `evaluar_postulacion()`.
- El funcionamiento de la API.
- La creación de registros.
- El modelo `Registro`.
- El borrado lógico.
- La autenticación.
- Los permisos del rol `viewer`.
- Los permisos del rol `normal`.
- Los permisos administrativos.
- La edición y recálculo del resultado.
- La eliminación lógica.

Al finalizar la implementación se ejecutó:

`python manage.py test`

Resultado obtenido:

- 20 pruebas ejecutadas.
- 20 pruebas aprobadas.
- Resultado final: `OK`.

## 9. Validación de las propuestas de IA

Las sugerencias realizadas con apoyo de Inteligencia Artificial no fueron consideradas correctas automáticamente.

Cada cambio fue revisado mediante:

- `python manage.py check`
- Migraciones de Django.
- Pruebas manuales desde el navegador.
- Django Admin.
- Pruebas de permisos mediante acceso directo a las URL.
- Pruebas automatizadas con `python manage.py test`.

Esto permitió verificar que las modificaciones fueran compatibles con el proyecto y que no alteraran la lógica original de evaluación.

## 10. Resultado

El uso de Inteligencia Artificial permitió apoyar el análisis y la implementación de mejoras, manteniendo la lógica original del proyecto.

El sistema final incorpora persistencia mediante base de datos, CRUD, borrado lógico, autenticación, roles, autorización y pruebas automatizadas, manteniendo la función original de evaluación como núcleo de la lógica de negocio.
