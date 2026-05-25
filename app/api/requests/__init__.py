"""Requests tipados para la API."""

from app.api.requests.leyenda_request import LeyendaRequest
from app.api.requests.turno_request import ProcesarTurnoRequest

__all__ = ["LeyendaRequest", "ProcesarTurnoRequest"]
