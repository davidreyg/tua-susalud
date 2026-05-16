# TUA SUSALUD

API para gestionar roles de turno y generar reportes con formato SUSALUD.

## Características clave

- Carga de archivos Excel con roles de turno.
- Procesamiento y validación de datos según normativa SUSALUD.
- Generación de reportes Excel con formato estándar SUSALUD.
- Almacenamiento de leyendas y configuraciones en PostgreSQL.
- API REST documentada con Swagger (/docs, /redoc).

## Arquitectura

`
[Cliente] --> [FastAPI] --> [Procesador Excel] --> [Reporte SUSALUD]
                 |
                 +--> [PostgreSQL]
`

1. FastAPI recibe el archivo Excel y lo valida.
2. TurnoService procesa los datos según las reglas de negocio.
3. Se genera un archivo Excel con el formato requerido por SUSALUD.
4. Las leyendas y configuraciones se persisten en PostgreSQL.

## Requisitos

- Python 3.10 o superior.
- [uv](https://docs.astral.sh/uv/) para instalar dependencias.
- PostgreSQL 13+.

## Variables de entorno

| Variable      | Descripción                           | Valor por defecto     |
| ------------- | ------------------------------------- | --------------------- |
| DB_SERVER   | Host de PostgreSQL.                   | localhost           |
| DB_PORT     | Puerto de PostgreSQL.                 | 5432                |
| DB_NAME     | Nombre de la base de datos.           | 	ua_susalud_db      |
| DB_USER     | Usuario de base de datos.             | postgres            |
| DB_PASSWORD | Contraseña del usuario de BD.         | 	ua_susalud_password|

Guarda estos valores en un archivo .env.local y cárgalo antes de iniciar el servicio.

## Instalación y ejecución local

`ash
git clone <repo-url>
cd tua-susalud
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

La API estará disponible en http://localhost:8000.

## Endpoints principales

| Método | Ruta        | Descripción                                |
| ------ | ----------- | ------------------------------------------ |
| GET    | /         | Información del servicio y rutas útiles.   |
| GET    | /health   | Verifica conectividad con la base de datos.|

## Comandos útiles

`ash
uv run pytest                # pruebas unitarias
uv run ruff check .          # linter
uv run ruff format .         # formateo automático
uv run pyright               # análisis estático
`

## Docker

`ash
docker build -t tua-susalud .
docker run --rm -p 8000:8000 --env-file .env.local tua-susalud
`

## Licencia

Este proyecto se distribuye bajo los términos de la licencia [MIT](LICENSE).

