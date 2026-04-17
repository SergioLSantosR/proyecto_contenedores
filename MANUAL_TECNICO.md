
================
## MANUAL TÉCNICO
================

## Manual técnico – Sistema de Puntos de Interés
## 1. Introducción

Este manual está dirigido a administradores y desarrolladores. Describe la arquitectura, configuración, despliegue, persistencia y localización de los componentes del sistema.
## 2. Arquitectura general

El sistema se compone de cuatro contenedores Docker orquestados con Docker Compose:

Contenedor	  Imagen / build        	Puerto interno	        Función
puntos_db	  postgis/postgis:15-3.4	5432	                Base de datos geoespacial
puntos_backend	  Construido desde backend/	8000	                API REST (FastAPI)
puntos_frontend	  Construido desde frontend/	80	                Servidor web estático (HTML/JS)
puntos_proxy	  nginx:alpine	                80 (expuesto)	        Proxy reverso (único punto de entrada)

Todos los contenedores se comunican a través de una red interna definida por el usuario: proyecto_contenedores_red-interna (driver bridge). Esta red permite la resolución de nombres por nombre de servicio (ej. backend → IP del contenedor backend).

## 3. Persistencia de datos
Se definen dos volúmenes Docker:

* datos-postgres: Almacena todos los datos de la base de datos (tablas, índices, configuraciones).
  Ubicación en el host (VM): /var/lib/docker/volumes/datos-postgres/_data
  Dentro del contenedor db: montado en /var/lib/postgresql/data

* logs-proxy: Almacena los logs de Nginx.
  Ubicación en el host: /var/lib/docker/volumes/logs-proxy/_data
  Dentro del contenedor proxy: montado en /var/log/nginx

Además, el archivo de configuración del proxy se monta como bind mount (lectura sola): 
./nginx-proxy/nginx.conf → /etc/nginx/conf.d/default.conf. 
Este archivo no es un volumen Docker, sino un archivo local del proyecto, por lo que su modificación requiere reconstruir el contenedor o reiniciarlo.

## 4. Configuración mediante variables de entorno
El archivo .env (no versionado) contiene las siguientes variables:

POSTGRES_USER=admin
POSTGRES_PASSWORD=seguro123
POSTGRES_DB=puntos_interes
DB_HOST=db
DB_PORT=5432
PROXY_PORT=80

Estas variables son referenciadas en docker-compose.yml y pasadas a los contenedores. El backend también las lee mediante os.getenv().

## 5. Despliegue paso a paso
5.1 Requisitos de la máquina virtual
	* Ubuntu 22.04 o superior.
	* Docker Engine (versión 20.10+) y Docker Compose Plugin instalados.
	* Usuario con permisos en el grupo docker (no usar sudo).
	* Puerto 80 libre (para Nginx dentro de la VM).
	* Reenvío de puertos en VirtualBox (opcional, para acceso desde el host): localhost:8080 → puerto 80 de la VM.

5.2 Instalación del proyecto
Copiar todos los archivos del proyecto a la MV, por ejemplo en ~/proyecto_contenedores.

Crear el archivo .env a partir de .env.example.

Ejecutar:

cd ~/proyecto_contenedores
docker compose build --no-cache
docker compose up -d

5.3 Verificación del funcionamiento
Verificar que los 4 contenedores estén Up:

docker compose ps
Probar la API:

curl http://localhost/api/puntos
Debe devolver un JSON con 5 puntos de interés precargados.

Acceder a la interfaz web: http://localhost:8080 (desde el host) o http://<IP_VM>.

## 6. Localización de la base de datos
La base de datos PostgreSQL+PostGIS se ejecuta dentro del contenedor puntos_db. Para conectarse directamente a la BD (por ejemplo, para depuración o consultas avanzadas):

docker exec -it puntos_db psql -U admin -d puntos_interes
Ubicación física de los archivos de la BD dentro del host (VM):
/var/lib/docker/volumes/datos-postgres/_data
Allí se encuentran los archivos como PG_VERSION, base/, global/, pg_wal/, etc.

Ubicación lógica dentro del contenedor:
/var/lib/postgresql/data

## 7. Mantenimiento y resolución de problemas comunes
7.1 Reiniciar el sistema después de apagar la MV

cd ~/proyecto_contenedores
docker compose up -d

7.2 Reconstruir solo el backend después de cambios en el código

docker compose build --no-cache backend
docker compose up -d

7.3 Ver logs de un contenedor específico

docker compose logs backend -f

7.4 Error de permisos al ejecutar docker
Asegúrate de que tu usuario pertenezca al grupo docker:

sudo usermod -aG docker $USER
newgrp docker

Cierra sesión y vuelve a abrirla.

7.5 El contenedor backend se detiene con Exited (1)
Revisa los logs:

docker compose logs backend --tail=50

El error más común era la indentación en main.py. Asegúrate de que el archivo esté corregido (ver sección de mejoras).

7.6 Error de iptables al crear la red
Cambia a iptables-legacy:

sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo systemctl restart docker

## 8. Mejoras implementadas durante el desarrollo
Frontend independiente: se separó del backend en su propio contenedor Nginx.

Corrección de indentación en main.py: se movió la creación de tablas al evento startup y se corrigió la indentación de get_db().

Eliminación del volumen montado en el backend: se quitó volumes: - ./backend:/app del docker-compose.yml para evitar que los archivos locales sobreescriban los de la imagen.

Corrección del proxy Nginx: se ajustó proxy_pass sin barra al final para preservar la ruta /api/.

Fijación de versión de NumPy: se agregó numpy==1.26.4 en requirements.txt para evitar conflictos con shapely.

Configuración de iptables-legacy para resolver conflictos de red en Ubuntu moderno.
