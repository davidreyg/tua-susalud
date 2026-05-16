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
        "Credenciales inválidas",
        "Porfavor intente mas tarde.",
    )
    PERMISSION_DENIED = (
        "PERM-403",
        "Permission denied.",
        "Access to this resource is forbidden.",
    )
