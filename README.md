================================================================================
## README.md
================================================================================

# Sistema de Puntos de Interés con Docker, Frontend Independiente y Alta Disponibilidad

## Descripción
Aplicación web para registrar y consultar puntos de interés geoespaciales (monumentos, estaciones de servicio, incidentes viales, etc.). El sistema está completamente contenerizado y orquestado con Docker Compose, incluyendo:

- *Base de datos geoespacial* PostgreSQL + PostGIS.
- *Backend API* desarrollado con FastAPI (Python).
- *Frontend independiente* con HTML/JS servido por Nginx.
- *Proxy reverso* Nginx que unifica el acceso: /api → backend, / → frontend.
- *Persistencia* mediante volúmenes Docker.
- *Red interna* definida por el usuario para comunicación entre contenedores.

## Requisitos previos
- Máquina virtual con Ubuntu (o cualquier sistema con Docker y Docker Compose).
- Docker Engine y Docker Compose Plugin instalados.
- Puertos necesarios: 80 (dentro de la VM) y 8080 (redirección desde el host).

## Estructura o diagrama del proyecto
proyecto_contenedores/
├── backend
│   ├── app
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── _init_.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── docker-stack.yml
├── frontend
│   ├── Dockerfile
│   └── static
│       └── index.html
├── MANUAL_TECNICO.md
├── MANUAL_USUARIO.md
├── nginx-proxy
│   └── nginx.conf
└── README.md


## Instalación y uso (en la MV)

1. Clona el repositorio o copia los archivos a la MV.
2. Crea el archivo .env a partir de .env.example y ajusta las contraseñas si lo deseas.
3. Ejecuta:
   
   docker compose up -d --build

4. Verifica que todos los contenedores estén en ejecución

   docker compose ps -a

5. Accede a la aplicación desde el navegador del host (configura el reenvío de puertos en VirtualBox: localhost:8080--> puerto 80 de la MV).

   URL: http://localhost:8080

## Detener el sistema

   docker compose down

Los datos de la base de datos persisten gracias al volumen datos-postgres. Para borrar también los datos, usar:
   docker compose down -v

## EndPoints de la API
* POST /api/puntos  --- Crear un punto (JSON con nombre, descripción, latitud, logitud, categoria).
* GET /api/puntos   --- Listar puntos. Parámetros adicionales:
   categoria (String)
   lat (float), lng (float), radio_km (float) -- búsqueda por proximidad.

