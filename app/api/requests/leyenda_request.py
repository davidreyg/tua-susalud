from pydantic import BaseModel


class LeyendaRequest(BaseModel):
    """Request para crear/actualizar una leyenda."""

    sigla: str
    nombre: str
    hora_inicio: str
    hora_fin: str
    cargo: str
