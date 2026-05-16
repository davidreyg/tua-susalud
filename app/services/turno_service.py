"""Servicio para procesamiento de archivos de roles de turno."""

from io import BytesIO
from typing import ClassVar

import pandas as pd


class TurnoService:
    """Servicio para procesar archivos Excel de roles de turno.

    Procesa un archivo .xlsx que contiene multiples hojas con datos de
    empleados, sus horarios y dias trabajados, y genera un archivo
    consolidado con la informacion estructurada.
    """

    # Columnas de identidad que se conservan en el resultado final.
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
        try:
            excel_file = pd.ExcelFile(BytesIO(input_bytes))
        except ValueError as exc:
            msg = f"No se pudo leer el archivo '{nombre_original}': {exc}"
            raise ValueError(msg) from exc

        nombres_hojas = excel_file.sheet_names

        if not nombres_hojas:
            msg = f"El archivo '{nombre_original}' no contiene hojas."
            raise ValueError(msg)

        min_columnas_validas = 2
        max_caracteres_pestana = 31
        resultados: list[tuple[pd.DataFrame, str]] = []

        for hoja in nombres_hojas:
            df_raw = pd.read_excel(excel_file, sheet_name=hoja, header=None)

            if df_raw.empty or len(df_raw.columns) < min_columnas_validas:
                continue

            cabecera_info = TurnoService._localizar_cabecera(df_raw)
            if cabecera_info is None:
                continue

            fila_4, fila_5, idx_data = cabecera_info
            cabecera = TurnoService._fusionar_cabeceras(fila_4, fila_5)

            df_datos = df_raw.iloc[idx_data:].copy()
            df_procesado = TurnoService._extraer_datos(df_datos, cabecera)

            if df_procesado is None or df_procesado.empty:
                continue

            nombre_pestana = (
                hoja[:max_caracteres_pestana]
                if isinstance(hoja, str)
                else str(hoja)[:max_caracteres_pestana]
            )
            resultados.append((df_procesado, nombre_pestana))

        if not resultados:
            msg = f"El archivo '{nombre_original}' no contiene datos validos."
            raise ValueError(msg)

        output_buffer = BytesIO()
        with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:  # type: ignore[arg-type]
            for df_procesado, nombre_pestana in resultados:
                df_procesado.to_excel(writer, index=False, sheet_name=nombre_pestana)

        output_buffer.seek(0)
        return output_buffer.getvalue()

    @staticmethod
    def _localizar_cabecera(
        df_raw: pd.DataFrame,
    ) -> tuple[pd.Series, pd.Series, int] | None:
        """Localiza las filas de cabecera en el DataFrame crudo.

        Busca la fila que contiene ``N°`` en la columna B (indice 1),
        devuelve esa fila, la siguiente (fila de dias) y el indice
        donde comienzan los datos.

        Args:
            df_raw: DataFrame con los datos crudos de una hoja.

        Returns:
            Tupla ``(fila_metadatos, fila_dias, idx_inicio_datos)`` o
            ``None`` si no se encontro la estructura esperada.

        """
        mascara = df_raw[1].astype(str).str.strip() == "N\u00b0"
        coincidencias = df_raw.loc[mascara]

        if coincidencias.empty:
            return None

        idx_fila_4: int = coincidencias.index[0]  # type: ignore[assignment]
        idx_fila_5: int = idx_fila_4 + 1

        if idx_fila_5 >= len(df_raw):
            return None

        fila_4 = df_raw.iloc[idx_fila_4].fillna("").astype(str).str.strip()
        fila_5 = df_raw.iloc[idx_fila_5].fillna("").astype(str).str.strip()

        return fila_4, fila_5, idx_fila_5 + 1

    @staticmethod
    def _fusionar_cabeceras(fila_4: pd.Series, fila_5: pd.Series) -> list[str]:
        """Fusiona dos filas de cabecera en una sola lista de nombres.

        Las columnas en los indices 1-4 (N°, NOMBRES, COND., CARG.) se
        toman de ``fila_4``. Las columnas siguientes (indice >4) toman
        el valor de ``fila_5`` con el prefijo ``"Día "``.

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
                cabecera.append(f"D\u00eda {fila_5.iloc[i]}")
            else:
                cabecera.append(f"COL_{i}")

        return cabecera

    @staticmethod
    def _extraer_datos(
        df_datos: pd.DataFrame, cabecera: list[str]
    ) -> pd.DataFrame | None:
        """Extrae y filtra los datos de empleados del DataFrame.

        Asigna los nombres de columna, filtra solo los registros con ID
        numerico y conserva solo las columnas de identidad y de dias.

        Args:
            df_datos: DataFrame con las filas de datos (ya sin las
                filas de cabecera).
            cabecera: Lista con los nombres de columna finales.

        Returns:
            DataFrame limpio con los datos de empleados, o ``None`` si
            no se encontraron registros validos.

        """
        df_datos.columns = cabecera

        col_id = cabecera[1]

        mascara_id = pd.to_numeric(df_datos[col_id], errors="coerce").notna()
        df_filtrado = df_datos.loc[mascara_id].copy()

        if df_filtrado.empty:
            return None

        df_filtrado[col_id] = pd.to_numeric(df_filtrado[col_id]).astype(int)

        cols_disponibles = set(df_filtrado.columns)
        cols_identidad = [
            c for c in TurnoService._COLUMNAS_IDENTIDAD if c in cols_disponibles
        ]
        cols_dias = [c for c in df_filtrado.columns if c.startswith("D\u00eda ")]
        cols_finales = cols_identidad + cols_dias

        df_final = df_filtrado[cols_finales].copy()

        for col in {"NOMBRES Y APELLIDOS", "CARG."} & set(df_final.columns):
            df_final[col] = df_final[col].astype(str).str.strip()

        return df_final
