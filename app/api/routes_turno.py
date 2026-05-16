"""Rutas para el procesamiento de roles de turno."""

from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.services.turno_service import TurnoService

router = APIRouter(prefix="/api/turno", tags=["Turno"])


@router.post(
    "/procesar",
    summary="Procesar archivo Excel de roles de turno",
    response_class=StreamingResponse,
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
        HTTPException 400: Si el archivo no es un .xlsx valido o el
            procesamiento falla.

    """
    if not archivo.filename or not archivo.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe tener extension .xlsx",
        )

    try:
        input_bytes = await archivo.read()
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Error al leer el archivo: {exc}",
        ) from exc

    if not input_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo esta vacio",
        )

    try:
        output_bytes = TurnoService.procesar_archivo(
            input_bytes,
            nombre_original=archivo.filename,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    nombre_descarga = archivo.filename.rsplit(".", 1)[0] + "_procesado.xlsx"

    return StreamingResponse(
        iter([output_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{nombre_descarga}"',
        },
    )
