from sqlmodel import Field, SQLModel


class Leyenda(SQLModel, table=True):
    """Modelo de base de datos."""

    id: int | None = Field(default=None, primary_key=True)
    sigla: str = Field(index=True, max_length=8)
    nombre: str
    hora_inicio: str
    hora_fin: str
    cargo: str
