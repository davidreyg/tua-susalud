from api_exception import BaseExceptionCode


class CustomExceptionCode(BaseExceptionCode):
    """Excepciones personalizadas para el API."""

    BAD_RESPONSE = (
        "API-422",
        "Respuesta del servicio invalida.",
        "Porfavor intente mas tarde.",
    )
    INVALID_CREDENTIALS = (
        "API-401",
        "Credenciales invalidas",
        "Porfavor intente mas tarde.",
    )
    PERMISSION_DENIED = (
        "PERM-403",
        "Permission denied.",
        "Access to this resource is forbidden.",
    )
    FILE_INVALID_EXTENSION = (
        "FILE-400",
        "Extension de archivo invalida.",
        "El archivo debe tener extension .xlsx.",
    )
    FILE_READ_ERROR = (
        "FILE-400",
        "Error al leer el archivo.",
        "No se pudo leer el archivo subido.",
    )
    FILE_EMPTY = (
        "FILE-400",
        "Archivo vacio.",
        "El archivo no contiene datos.",
    )
    FILE_PROCESSING_ERROR = (
        "FILE-422",
        "Error al procesar el archivo.",
        "El archivo no tiene el formato esperado o no contiene datos validos.",
    )
    SHEET_NOT_FOUND = (
        "SHEET-404",
        "Hoja no encontrada.",
        "La hoja especificada no existe en el archivo Excel.",
    )
    INVALID_SHEET_NAME = (
        "SHEET-400",
        "Nombre de hoja invalido.",
        "El nombre de la hoja no puede estar vacio.",
    )
    DATA_EMPTY = (
        "DATA-400",
        "No hay datos para procesar.",
        "La lista de datos enviada esta vacia.",
    )
    DATA_TOO_LARGE = (
        "DATA-413",
        "Demasiados registros.",
        "La cantidad de registros supera el limite permitido.",
    )
    DATA_WRITE_ERROR = (
        "DATA-500",
        "Error al escribir los datos.",
        "No se pudo generar el archivo Excel.",
    )
