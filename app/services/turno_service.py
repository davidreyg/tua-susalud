"""Servicio para procesamiento de archivos de roles de turno."""

from io import BytesIO
from typing import ClassVar

import pandas as pd

from tools.logger import Logger

logger = Logger(__name__)


class TurnoService:
    """Servicio para procesar archivos Excel de roles de turno.

    Procesa un archivo .xlsx que contiene multiples hojas con datos de
    empleados, sus horarios y dias trabajados, y genera un archivo
    consolidado con la informacion estructurada.
    """

    _COLUMNAS_IDENTIDAD: ClassVar[list[str]] = [
        "N\u00b0",
        "NOMBRES Y APELLIDOS",
        "COND.",
        "CARG.",
    ]

    @staticmethod
    def procesar_archivo(
        input_bytes: bytes, nombre_original: str = "reporte.xlsx"
    ) -> bytes:
        """Procesa un archivo Excel con roles de turno y retorna el resultado.

        Lee todas las hojas del archivo, extrae la cabecera compuesta
        (fila de metadatos + fila de dias), filtra los registros de
        empleados y consolida todo en un unico archivo Excel.

        Args:
            input_bytes: Contenido binario del archivo Excel de entrada.
            nombre_original: Nombre original del archivo (se usa solo
                como referencia en logs).

        Returns:
            Contenido binario del archivo Excel procesado.

        Raises:
            ValueError: Si el archivo esta vacio, no tiene hojas validas
                o no se encuentra la estructura esperada.

        """
        logger.info("Iniciando procesamiento del archivo '%s'...", nombre_original)

        try:
            excel_file = pd.ExcelFile(BytesIO(input_bytes))
        except ValueError as exc:
            logger.exception("No se pudo leer el archivo '%s'", nombre_original)
            msg = f"No se pudo leer el archivo '{nombre_original}': {exc}"
            raise ValueError(msg) from exc

        nombres_hojas = excel_file.sheet_names
        logger.info(
            "Archivo '%s' cargado correctamente (%d hoja(s))",
            nombre_original,
            len(nombres_hojas),
        )

        if not nombres_hojas:
            logger.warning("El archivo '%s' no contiene hojas.", nombre_original)
            msg = f"El archivo '{nombre_original}' no contiene hojas."
            raise ValueError(msg)

        min_columnas_validas = 2
        max_caracteres_pestana = 31
        resultados: list[tuple[pd.DataFrame, str]] = []

        for hoja in nombres_hojas:
            nombre_hoja = str(hoja)
            logger.info("Procesando hoja: '%s'...", nombre_hoja)
            df_raw = pd.read_excel(excel_file, sheet_name=hoja, header=None)

            if df_raw.empty or len(df_raw.columns) < min_columnas_validas:
                logger.warning("Hoja '%s' vacia o invalida. Omitiendo.", nombre_hoja)
                continue

            cabecera_info = TurnoService._localizar_cabecera(df_raw, nombre_hoja)
            if cabecera_info is None:
                continue

            fila_4, fila_5, idx_data = cabecera_info
            cabecera = TurnoService._fusionar_cabeceras(fila_4, fila_5)

            df_datos = df_raw.iloc[idx_data:].copy()
            df_procesado = TurnoService._extraer_datos(df_datos, cabecera, nombre_hoja)

            if df_procesado is None or df_procesado.empty:
                continue

            nombre_pestana = nombre_hoja[:max_caracteres_pestana]
            resultados.append((df_procesado, nombre_pestana))

            logger.info(
                "Hoja '%s' procesada con exito (%d empleado(s)).",
                hoja,
                len(df_procesado),
            )

        if not resultados:
            logger.warning(
                "El archivo '%s' no contiene datos validos en ninguna hoja.",
                nombre_original,
            )
            msg = f"El archivo '{nombre_original}' no contiene datos validos."
            raise ValueError(msg)

        logger.info(
            "Escribiendo %d hoja(s) en el archivo de salida...", len(resultados)
        )

        output_buffer = BytesIO()
        with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:  # type: ignore[arg-type]
            for df_procesado, nombre_pestana in resultados:
                df_procesado.to_excel(writer, index=False, sheet_name=nombre_pestana)
                logger.debug(
                    "Pestana '%s' escrita (%d registro(s)).",
                    nombre_pestana,
                    len(df_procesado),
                )

        output_buffer.seek(0)

        total_empleados = sum(len(df) for df, _ in resultados)
        logger.info(
            "Proceso finalizado. Archivo '%s' generado (%d hoja(s), %d empleado(s)).",
            nombre_original,
            len(resultados),
            total_empleados,
        )

        return output_buffer.getvalue()

    @staticmethod
    def _localizar_cabecera(
        df_raw: pd.DataFrame, nombre_hoja: str = "?"
    ) -> tuple[pd.Series, pd.Series, int] | None:
        """Localiza las filas de cabecera en el DataFrame crudo.

        Busca la fila que contiene ``N°`` en la columna B (indice 1),
        devuelve esa fila, la siguiente (fila de dias) y el indice
        donde comienzan los datos.

        Args:
            df_raw: DataFrame con los datos crudos de una hoja.
            nombre_hoja: Nombre de la hoja para los mensajes de log.

        Returns:
            Tupla ``(fila_metadatos, fila_dias, idx_inicio_datos)`` o
            ``None`` si no se encontro la estructura esperada.

        """
        mascara = df_raw[1].astype(str).str.strip() == "N\u00b0"
        coincidencias = df_raw.loc[mascara]

        if coincidencias.empty:
            logger.warning(
                "No se encontro la celda 'N°' en columna B de la hoja '%s'. Omitiendo.",
                nombre_hoja,
            )
            return None

        idx_fila_4: int = coincidencias.index[0]  # type: ignore[assignment]
        idx_fila_5: int = idx_fila_4 + 1

        if idx_fila_5 >= len(df_raw):
            logger.warning(
                "Estructura incompleta en la hoja '%s' (falta fila de dias). "
                "Omitiendo.",
                nombre_hoja,
            )
            return None

        fila_4 = df_raw.iloc[idx_fila_4].fillna("").astype(str).str.strip()
        fila_5 = df_raw.iloc[idx_fila_5].fillna("").astype(str).str.strip()

        return fila_4, fila_5, idx_fila_5 + 1

    @staticmethod
    def _fusionar_cabeceras(fila_4: pd.Series, fila_5: pd.Series) -> list[str]:
        """Fusiona dos filas de cabecera en una sola lista de nombres.

        Las columnas en los indices 1-4 (N°, NOMBRES, COND., CARG.) se
        toman de ``fila_4``. Las columnas siguientes (indice >4) toman
        directamente el valor numerico de ``fila_5``.

        Args:
            fila_4: Fila de metadatos (contiene los nombres fijos).
            fila_5: Fila de dias (contiene los numeros de dia).

        Returns:
            Lista con los nombres de columna finales.

        """
        cabecera: list[str] = []
        limite = 4
        for i in range(len(fila_4)):
            if i in {1, 2, 3, 4}:
                valor = fila_4.iloc[i] or f"COL_{i}"
                cabecera.append(str(valor))
            elif i > limite and fila_5.iloc[i] != "":
                cabecera.append(str(fila_5.iloc[i]))
            else:
                cabecera.append(f"COL_{i}")

        return cabecera

    @staticmethod
    def _extraer_datos(
        df_datos: pd.DataFrame,
        cabecera: list[str],
        nombre_hoja: str = "?",
    ) -> pd.DataFrame | None:
        """Extrae y filtra los datos de empleados del DataFrame.

        Asigna los nombres de columna, filtra solo los registros con ID
        numerico y conserva solo las columnas de identidad y de dias.

        Args:
            df_datos: DataFrame con las filas de datos (ya sin las
                filas de cabecera).
            cabecera: Lista con los nombres de columna finales.
            nombre_hoja: Nombre de la hoja para los mensajes de log.

        Returns:
            DataFrame limpio con los datos de empleados, o ``None`` si
            no se encontraron registros validos.

        """
        df_datos.columns = cabecera

        col_id = cabecera[1]

        mascara_id = pd.to_numeric(df_datos[col_id], errors="coerce").notna()
        df_filtrado = df_datos.loc[mascara_id].copy()

        if df_filtrado.empty:
            logger.warning(
                "No se encontraron registros de empleados en la hoja '%s'. Omitiendo.",
                nombre_hoja,
            )
            return None

        df_filtrado[col_id] = pd.to_numeric(df_filtrado[col_id]).astype(int)

        cols_disponibles = set(df_filtrado.columns)
        cols_identidad = [
            c for c in TurnoService._COLUMNAS_IDENTIDAD if c in cols_disponibles
        ]
        cols_dias = [c for c in df_filtrado.columns if str(c).strip().isdigit()]
        cols_finales = cols_identidad + cols_dias

        df_final = df_filtrado[cols_finales].copy()

        for col in {"NOMBRES Y APELLIDOS", "CARG."} & set(df_final.columns):
            df_final[col] = df_final[col].astype(str).str.strip()

        logger.debug(
            "Datos extraidos en '%s': %d fila(s), %d columna(s)",
            nombre_hoja,
            len(df_final),
            len(cols_finales),
        )

        return df_final
