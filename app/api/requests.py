from pydantic import BaseModel
from sqlmodel import Field


class ProcesarTurnoRequest(BaseModel):
    """Request para procesar archivo de roles de turno."""

    archivo_excel: bytes = Field(..., description="Archivo Excel con roles de turno")
    periodo: str = Field(..., description="Periodo en formato YYYYMM")
