from sqlmodel import Session, col, select

from app.models.leyenda import Leyenda


class LeyendaRepository:
    """Repositorio para el modelo Leyenda."""

    def __init__(self, session: Session) -> None:
        """Inicio."""
        self.session = session

    def get_all(self) -> list[Leyenda]:
        """Obtener todas las leyendas."""
        return list(self.session.exec(select(Leyenda)).all())

    def get_by_id(self, leyenda_id: int) -> Leyenda | None:
        """Obtener una leyenda por su ID."""
        return self.session.get(Leyenda, leyenda_id)

    def get_by_sigla(self, sigla: str) -> Leyenda | None:
        """Obtener una leyenda por su sigla."""
        stmt = select(Leyenda).where(col(Leyenda.sigla) == sigla)
        return self.session.exec(stmt).first()

    def create(self, leyenda: Leyenda) -> Leyenda:
        """Crear una nueva leyenda."""
        self.session.add(leyenda)
        self.session.commit()
        self.session.refresh(leyenda)
        return leyenda

    def update(self, leyenda: Leyenda) -> Leyenda:
        """Actualizar una leyenda existente."""
        self.session.add(leyenda)
        self.session.commit()
        self.session.refresh(leyenda)
        return leyenda

    def delete(self, leyenda: Leyenda) -> None:
        """Eliminar una leyenda."""
        self.session.delete(leyenda)
        self.session.commit()
