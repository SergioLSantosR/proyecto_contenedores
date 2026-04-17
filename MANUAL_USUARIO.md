================================================================================
## MANUAL DE USUARIO
================================================================================

## Manual de usuario – Sistema de Puntos de Interés
1. Acceso a la aplicación
Abre tu navegador web (Chrome, Firefox, Edge) y escribe la siguiente dirección:

text
http://localhost:8080
Nota: Si el sistema está desplegado en una máquina virtual con VirtualBox, debes haber configurado el reenvío de puertos (host 8080 → VM 80). En caso de tener una IP directa, usa http://<IP_de_la_VM>.

2. Interfaz principal
La pantalla se divide en dos secciones:

Formulario de registro de nuevo punto (arriba).

Panel de consulta y filtros (abajo), que muestra los resultados.

(Puedes agregar una captura de pantalla de tu aplicación aquí)

3. Registrar un nuevo punto de interés
Completa los campos:

Nombre (obligatorio, ej. "Museo Nacional").

Descripción (opcional, ej. "Exposición de arte contemporáneo").

Latitud (número decimal, ej. -34.6037).

Longitud (número decimal, ej. -58.3816).

Categoría (selecciona entre: cultural, gastronómico, natural, servicio).

Haz clic en el botón "Registrar Punto".

Si todo es correcto, aparecerá un mensaje de éxito y la lista se actualizará automáticamente mostrando el nuevo punto.

4. Consultar puntos de interés
4.1 Listar todos los puntos
Haz clic en el botón "Listar todos". Se mostrarán todos los puntos registrados (incluyendo los 5 de ejemplo y los que hayas agregado).

4.2 Filtrar por categoría
En el campo "Filtrar por categoría", escribe una categoría (ej. "cultural") y haz clic en "Buscar con filtros". Solo aparecerán los puntos de esa categoría.

4.3 Búsqueda por proximidad (radio)
Para encontrar puntos cercanos a una ubicación dada:

Introduce la latitud y longitud del centro de búsqueda.

Introduce el radio de búsqueda en kilómetros.

Haz clic en "Buscar con filtros".

El sistema devolverá los puntos que se encuentren dentro de ese radio (usando la capacidad geoespacial de PostGIS).

4.4 Combinar filtros
Puedes usar simultáneamente el filtro por categoría y la búsqueda por radio. Solo debes completar ambos campos y hacer clic en "Buscar con filtros".

5. Visualización de resultados
Cada punto se muestra como una tarjeta que contiene:

Nombre (en negrita).

Categoría (entre paréntesis).

Descripción (si se proporcionó).

Coordenadas (latitud, longitud).

6. Mensajes de error
"Error de conexión": Indica que el backend no está respondiendo. Verifica que los contenedores estén corriendo (contacta al administrador).

"Error: debe proporcionar latitud y longitud": Aparece cuando se ingresa radio pero falta latitud o longitud.

"Error: punto creado exitosamente" (es un éxito, no un error).

7. Limitaciones conocidas
La búsqueda por proximidad asume una Tierra plana (para distancias cortas es precisa). No se ha implementado el cálculo de distancia esférica, pero es aceptable para un proyecto académico.

No hay autenticación de usuarios (toda persona con acceso a la URL puede registrar o consultar puntos).

8. Soporte
Para problemas técnicos, contacta al administrador del sistema. Incluye en tu reporte:

El mensaje de error completo.

Si es posible, una captura de pantalla.

El comando docker compose ps y docker compose logs backend (si tienes acceso a la MV).

¡Gracias por usar el Sistema de Puntos de Interés!
