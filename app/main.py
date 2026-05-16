from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api_exception import (
    register_exception_handlers,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tools.logger import Logger

from .database import db_config

# Configurar logging
logger = Logger(__name__)


# Contexto de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    """Contexto de vida de la aplicación."""
    # Startup
    logger.info("🚀 Iniciando aplicación TUA SUSALUD...")

    # Probar conexión a la base de datos PostgreSQL
    if db_config.test_connection():
        logger.info("✅ Conexión a PostgreSQL establecida")
    else:
        logger.info("❌ Error al conectar con PostgreSQL")

    yield
    db_config.close()

    # Shutdown
    logger.info("🛑 Cerrando aplicación TUA SUSALUD...")


# Crear la aplicación FastAPI
app = FastAPI(
    title="TUA SUSALUD API",
    description="API para gestionar roles de turno y generar reportes SUSALUD",
    version="1.0.0",
    lifespan=lifespan,
)
# Register exception handlers globally to have the consistent
# error handling and response structure
register_exception_handlers(app=app, use_fallback_middleware=True)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    """Endpoint raíz de la API."""
    return {
        "message": "API de TUA SUSALUD - Gestión de Roles de Turno",
        "version": "1.0.0",
        "database": "PostgreSQL",
        "endpoints": [
            "/docs - Documentación Swagger",
            "/redoc - Documentación ReDoc",
            # Agregar aquí tus endpoints específicos
        ],
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Endpoint para verificar el estado de la aplicación."""
    db_status = db_config.test_connection()

    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "service": "tua-susalud",
    }
