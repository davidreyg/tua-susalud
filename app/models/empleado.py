"""Modelo de base de datos para empleados."""

from sqlmodel import Field, SQLModel


class Empleado(SQLModel, table=True):
    """Modelo de base de datos para empleados/profesionales de salud."""

    id: int | None = Field(default=None, primary_key=True)
    tipo_documento: str = Field(max_length=10)
    numero_documento: str = Field(index=True, max_length=20)
    apellidos: str
    nombres: str
    nombre_completo: str
    profesion: str
    numero_de_colegiatura: str = Field(max_length=20)
    especialidad: str
    servicio: str
