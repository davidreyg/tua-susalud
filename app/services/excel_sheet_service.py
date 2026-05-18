"""Servicio para lectura de hojas específicas en archivos Excel."""

from io import BytesIO
from typing import Any

import pandas as pd

from tools.logger import Logger

logger = Logger(__name__)


class ExcelSheetService:
    """Servicio para leer hojas específicas de archivos Excel."""

    @staticmethod
    def _resolver_hoja(
        hojas_disponibles: list[str],
        identificador: str,
    ) -> str:
        """Resuelve el identificador de hoja (nombre o índice) a un nombre.

        Si el identificador es numérico se interpreta como índice
        1-based (1 = primera hoja). Si no, se busca por nombre exacto.

        Args:
            hojas_disponibles: Lista de nombres de hojas del archivo.
            identificador: Nombre de la hoja o índice 1-based.

        Returns:
            Nombre de la hoja a leer.

        Raises:
            ValueError: Si el identificador no corresponde a ninguna hoja.

        """
        if identificador.isdigit():
            idx = int(identificador) - 1
            if 0 <= idx < len(hojas_disponibles):
                return str(hojas_disponibles[idx])
            logger.warning(
                "Índice %d fuera de rango (1-%d).",
                int(identificador),
                len(hojas_disponibles),
            )
            msg = (
                f"Índice {identificador} fuera de rango. "
                f"El archivo tiene {len(hojas_disponibles)} hoja(s)."
            )
            raise ValueError(msg)

        if identificador in hojas_disponibles:
            return identificador

        hojas_str = ", ".join(hojas_disponibles)
        logger.warning(
            "Hoja '%s' no encontrada. Hojas disponibles: %s",
            identificador,
            hojas_str,
        )
        msg = (
            f"La hoja '{identificador}' no existe en el archivo. "
            f"Hojas disponibles: {hojas_str}"
        )
        raise ValueError(msg)

    @staticmethod
    def obtener_hoja(
        input_bytes: bytes, hoja: str, nombre_archivo: str = "archivo.xlsx"
    ) -> dict[str, Any]:
        """Lee una hoja específica de un archivo Excel y retorna sus datos.

        La hoja se puede identificar por nombre exacto o por índice
        1-based (1 = primera hoja, 2 = segunda, etc.).

        Args:
            input_bytes: Contenido binario del archivo Excel.
            hoja: Nombre exacto de la hoja o índice 1-based.
            nombre_archivo: Nombre original del archivo para logs.

        Returns:
            Diccionario con ``nombre_hoja``, ``filas`` y ``datos``.

        Raises:
            ValueError: Si la hoja no existe, el archivo no se puede leer
                o la hoja está vacía.

        """
        logger.info("Leyendo hoja '%s' del archivo '%s'...", hoja, nombre_archivo)

        try:
            excel_file = pd.ExcelFile(BytesIO(input_bytes))
        except ValueError as exc:
            logger.exception("No se pudo leer el archivo '%s'", nombre_archivo)
            msg = f"No se pudo leer el archivo '{nombre_archivo}': {exc}"
            raise ValueError(msg) from exc

        hojas_disponibles: list[str] = [str(h) for h in excel_file.sheet_names]
        logger.info(
            "Archivo '%s' contiene %d hoja(s): %s",
            nombre_archivo,
            len(hojas_disponibles),
            ", ".join(hojas_disponibles),
        )

        nombre_hoja = ExcelSheetService._resolver_hoja(hojas_disponibles, hoja)
        logger.info(
            "Hoja '%s' resuelta (identificador: '%s'), leyendo datos...",
            nombre_hoja,
            hoja,
        )

        df = pd.read_excel(excel_file, sheet_name=nombre_hoja)

        if df.empty:
            logger.warning("La hoja '%s' no contiene datos.", nombre_hoja)
            msg = f"La hoja '{nombre_hoja}' no contiene datos."
            raise ValueError(msg)

        datos = df.to_dict(orient="records")

        logger.info(
            "Hoja '%s' leida exitosamente (%d fila(s), %d columna(s)).",
            nombre_hoja,
            len(datos),
            len(df.columns),
        )

        return {
            "nombre_hoja": nombre_hoja,
            "filas": len(datos),
            "datos": datos,
        }

    @staticmethod
    def listar_hojas(
        input_bytes: bytes, nombre_archivo: str = "archivo.xlsx"
    ) -> list[str]:
        """Retorna los nombres de todas las hojas de un archivo Excel.

        Args:
            input_bytes: Contenido binario del archivo Excel.
            nombre_archivo: Nombre original del archivo para logs.

        Returns:
            Lista con los nombres de las hojas disponibles.

        Raises:
            ValueError: Si el archivo no se puede leer.

        """
        logger.info("Listando hojas del archivo '%s'...", nombre_archivo)

        try:
            excel_file = pd.ExcelFile(BytesIO(input_bytes))
        except ValueError as exc:
            logger.exception("No se pudo leer el archivo '%s'", nombre_archivo)
            msg = f"No se pudo leer el archivo '{nombre_archivo}': {exc}"
            raise ValueError(msg) from exc

        nombres: list[str] = [str(n) for n in excel_file.sheet_names]
        logger.info(
            "Archivo '%s' tiene %d hoja(s): %s",
            nombre_archivo,
            len(nombres),
            ", ".join(nombres),
        )

        return nombres
