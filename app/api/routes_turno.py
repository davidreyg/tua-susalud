"""Rutas para el procesamiento de roles de turno."""

from typing import Annotated

from api_exception import APIException, APIResponse
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from app.api.exceptions import CustomExceptionCode
from app.services.turno_service import TurnoService

router = APIRouter(prefix="/api/turno", tags=["Turno"])


@router.post(
    "/procesar",
    summary="Procesar archivo Excel de roles de turno",
    response_class=StreamingResponse,
    responses=APIResponse.default(),  # type: ignore
)
async def procesar_archivo(
    archivo: Annotated[
        UploadFile,
        File(description="Archivo Excel (.xlsx) con roles de turno"),
    ],
) -> StreamingResponse:
    """Procesa un archivo Excel con roles de turno y descarga el resultado.

    Recibe un archivo .xlsx que contiene una o varias hojas con datos
    de empleados (horarios, dias trabajados), extrae y estructura la
    informacion, y devuelve un archivo Excel limpio para descargar.

    Args:
        archivo: Archivo Excel subido por el usuario.

    Returns:
        Respuesta binaria con el archivo Excel procesado.

    Raises:
        APIException: Si el archivo no es valido o el procesamiento falla.

    """
    if not archivo.filename or not archivo.filename.lower().endswith(".xlsx"):
        raise APIException(
            error_code=CustomExceptionCode.FILE_INVALID_EXTENSION,
            http_status_code=400,
        )

    try:
        input_bytes = await archivo.read()
    except Exception as exc:
        raise APIException(
            error_code=CustomExceptionCode.FILE_READ_ERROR,
            http_status_code=400,
        ) from exc

    if not input_bytes:
        raise APIException(
            error_code=CustomExceptionCode.FILE_EMPTY,
            http_status_code=400,
        )

    try:
        output_bytes = TurnoService.procesar_archivo(
            input_bytes,
            nombre_original=archivo.filename,
        )
    except ValueError as exc:
        raise APIException(
            error_code=CustomExceptionCode.FILE_PROCESSING_ERROR,
            http_status_code=422,
        ) from exc

    nombre_descarga = archivo.filename.rsplit(".", 1)[0] + "_procesado.xlsx"

    return StreamingResponse(
        iter([output_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{nombre_descarga}"',
        },
    )
