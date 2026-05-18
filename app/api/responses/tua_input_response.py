"""Modelos de respuesta para datos de entrada TUA."""

from pydantic import BaseModel


class TurnoItem(BaseModel):
    """Turno asignado a un profesional en un dia especifico."""

    dia: int
    hora_entrada: str | None = None
    hora_salida: str | None = None


class TuaInputDataResponse(BaseModel):
    """Modelo tipado para datos de entrada TUA procesados.

    Representa un registro consolidado de un profesional de salud
    con su información personal, establecimiento y turnos asignados.
    """

    codigo_unico: str
    nombre_establecimiento: str
    red: str
    tipo_documento: str
    numero_documento: str
    profesion: str
    numero_colegiatura: str
    apellidos: str
    nombres: str
    especialidad: str
    servicio: str
    turnos: list[TurnoItem]
