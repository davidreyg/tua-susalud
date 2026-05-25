from api_exception import APIException
from sqlmodel import Session

from app.api.exceptions import CustomExceptionCode
from app.api.requests.leyenda_request import LeyendaRequest
from app.models.leyenda import Leyenda
from app.repositories.leyenda import LeyendaRepository


class LeyendaService:
    """Servicio para operaciones CRUD de leyendas."""

    @staticmethod
    def listar(session: Session) -> list[Leyenda]:
        """Obtener todas las leyendas."""
        return LeyendaRepository(session).get_all()

    @staticmethod
    def obtener(session: Session, leyenda_id: int) -> Leyenda:
        """Obtener una leyenda por su ID."""
        leyenda = LeyendaRepository(session).get_by_id(leyenda_id)
        if not leyenda:
            raise APIException(
                error_code=CustomExceptionCode.LEYENDA_NOT_FOUND,
                http_status_code=404,
            )
        return leyenda

    @staticmethod
    def crear(session: Session, data: LeyendaRequest) -> Leyenda:
        """Crear una nueva leyenda."""
        leyenda = Leyenda(**data.model_dump())
        return LeyendaRepository(session).create(leyenda)

    @staticmethod
    def actualizar(session: Session, leyenda_id: int, data: LeyendaRequest) -> Leyenda:
        """Actualizar una leyenda existente."""
        repo = LeyendaRepository(session)
        leyenda = repo.get_by_id(leyenda_id)
        if not leyenda:
            raise APIException(
                error_code=CustomExceptionCode.LEYENDA_NOT_FOUND,
                http_status_code=404,
            )
        for field, value in data.model_dump().items():
            setattr(leyenda, field, value)
        return repo.update(leyenda)

    @staticmethod
    def eliminar(session: Session, leyenda_id: int) -> None:
        """Eliminar una leyenda por su ID."""
        repo = LeyendaRepository(session)
        leyenda = repo.get_by_id(leyenda_id)
        if not leyenda:
            raise APIException(
                error_code=CustomExceptionCode.LEYENDA_NOT_FOUND,
                http_status_code=404,
            )
        repo.delete(leyenda)
