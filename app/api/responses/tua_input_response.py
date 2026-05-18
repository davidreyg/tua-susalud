"""Modelos de respuesta para datos de entrada TUA."""

from pydantic import BaseModel


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
    turnos: dict[int, tuple[str, str]]
