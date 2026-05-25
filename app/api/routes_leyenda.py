from typing import Annotated

from api_exception import APIResponse
from fastapi import APIRouter, Path

from app.api.requests.leyenda_request import LeyendaRequest
from app.models.leyenda import Leyenda
from app.services.leyenda_service import LeyendaService

router = APIRouter(prefix="/leyendas", tags=["Leyendas"])


@router.get(
    "/",
    summary="Listar todas las leyendas",
    responses=APIResponse.default(),  # type: ignore
)
async def listar_leyendas() -> list[Leyenda]:
    """Retorna la lista completa de leyendas registradas."""
    from app.database import get_database_config

    db_config = get_database_config()
    session = db_config.get_session()
    try:
        return LeyendaService.listar(session)
    finally:
        session.close()


@router.get(
    "/{leyenda_id}",
    summary="Obtener una leyenda por ID",
    responses=APIResponse.default(),  # type: ignore
)
async def obtener_leyenda(
    leyenda_id: Annotated[int, Path(description="ID de la leyenda")],
) -> Leyenda:
    """Retorna una leyenda por su ID."""
    from app.database import get_database_config

    db_config = get_database_config()
    session = db_config.get_session()
    try:
        return LeyendaService.obtener(session, leyenda_id)
    finally:
        session.close()


@router.post(
    "/",
    status_code=201,
    summary="Crear una nueva leyenda",
    responses=APIResponse.default(),  # type: ignore
)
async def crear_leyenda(data: LeyendaRequest) -> Leyenda:
    """Crea una nueva leyenda y la retorna."""
    from app.database import get_database_config

    db_config = get_database_config()
    session = db_config.get_session()
    try:
        return LeyendaService.crear(session, data)
    finally:
        session.close()


@router.put(
    "/{leyenda_id}",
    summary="Actualizar una leyenda existente",
    responses=APIResponse.default(),  # type: ignore
)
async def actualizar_leyenda(
    leyenda_id: Annotated[int, Path(description="ID de la leyenda")],
    data: LeyendaRequest,
) -> Leyenda:
    """Actualiza una leyenda por su ID y la retorna."""
    from app.database import get_database_config

    db_config = get_database_config()
    session = db_config.get_session()
    try:
        return LeyendaService.actualizar(session, leyenda_id, data)
    finally:
        session.close()


@router.delete(
    "/{leyenda_id}",
    status_code=204,
    summary="Eliminar una leyenda",
    responses=APIResponse.default(),  # type: ignore
)
async def eliminar_leyenda(
    leyenda_id: Annotated[int, Path(description="ID de la leyenda")],
) -> None:
    """Elimina una leyenda por su ID."""
    from app.database import get_database_config

    db_config = get_database_config()
    session = db_config.get_session()
    try:
        LeyendaService.eliminar(session, leyenda_id)
    finally:
        session.close()
