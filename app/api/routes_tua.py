"""Rutas para el procesamiento de roles de turno."""

from typing import Annotated

from api_exception import APIException, APIResponse
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from app.api.exceptions import CustomExceptionCode
from app.services.excel_sheet_service import ExcelSheetService
from app.services.turno_service import TurnoService

router = APIRouter(prefix="/tua", tags=["TUA SUSALUD"])


@router.post(
    "/limpiar-roles-turno",
    summary="Procesar archivo Excel de roles de turno",
    response_class=StreamingResponse,
    responses=APIResponse.default(),  # type: ignore
)
async def limpiar_roles(
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


@router.post(
    "/leer-excel-roles",
    summary="Leer una hoja específica de un archivo Excel",
    responses=APIResponse.default(),  # type: ignore
)
async def leer_hoja(
    archivo: Annotated[
        UploadFile,
        File(description="Archivo Excel (.xlsx)"),
    ],
    hoja: Annotated[
        str,
        Form(description="Nombre de la hoja o índice 1-based (ej: '1', '2')"),
    ],
) -> dict:
    """Lee los datos de una hoja específica de un archivo Excel.

    Recibe un archivo .xlsx y el identificador de la hoja que se desea
    leer. La hoja se puede identificar por nombre exacto o por índice
    1-based (1 = primera hoja, 2 = segunda, etc.).

    Args:
        archivo: Archivo Excel subido por el usuario.
        hoja: Nombre exacto de la hoja o índice 1-based.

    Returns:
        Diccionario con el nombre de la hoja, cantidad de filas y los datos.

    Raises:
        APIException: Si el archivo no es valido, la hoja no existe
            o ocurre un error durante el procesamiento.

    """
    if not archivo.filename or not archivo.filename.lower().endswith(".xlsx"):
        raise APIException(
            error_code=CustomExceptionCode.FILE_INVALID_EXTENSION,
            http_status_code=400,
        )

    if not hoja.strip():
        raise APIException(
            error_code=CustomExceptionCode.INVALID_SHEET_NAME,
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
        resultado = ExcelSheetService.obtener_hoja(
            input_bytes=input_bytes,
            hoja=hoja,
            nombre_archivo=archivo.filename,
        )
    except ValueError as exc:
        error_msg = str(exc).lower()
        if "no existe" in error_msg or "fuera de rango" in error_msg:
            raise APIException(
                error_code=CustomExceptionCode.SHEET_NOT_FOUND,
                http_status_code=404,
            ) from exc
        raise APIException(
            error_code=CustomExceptionCode.FILE_PROCESSING_ERROR,
            http_status_code=422,
        ) from exc

    return resultado
