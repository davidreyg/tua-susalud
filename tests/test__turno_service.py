"""Tests para el servicio de procesamiento de turnos."""

from io import BytesIO

import pandas as pd
import pytest

from app.services.turno_service import TurnoService


def _generar_excel_valido(hojas: list[list[list[str]]] | None = None) -> bytes:
    """Genera un archivo Excel de prueba con estructura valida.

    Args:
        hojas: Lista de hojas. Si es ``None`` se usa una hoja por defecto.

    Returns:
        Contenido binario del archivo Excel.

    """
    if hojas is None:
        hojas = [
            [
                ["", "", "", "", "", "", ""],
                ["", "", "", "", "", "", ""],
                ["", "N\u00b0", "NOMBRES Y APELLIDOS", "COND.", "CARG.", "", ""],
                ["", "", "", "", "", "1", "2"],
                ["", "1", "JUAN PEREZ", "A", "OPERARIO", "X", ""],
                ["", "2", "MARIA GOMEZ", "B", "SUPERVISOR", "", "X"],
            ],
        ]

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:  # type: ignore[arg-type]
        for i, hoja in enumerate(hojas):
            df = pd.DataFrame(hoja)
            df.to_excel(writer, index=False, header=False, sheet_name=f"Hoja{i + 1}")

    buffer.seek(0)
    return buffer.getvalue()


class TestTurnoService:
    """Tests para TurnoService."""

    def test_procesar_archivo_valido(self) -> None:
        """Debe procesar un archivo valido y retornar un Excel con datos."""
        input_bytes = _generar_excel_valido()
        output_bytes = TurnoService.procesar_archivo(input_bytes)

        assert isinstance(output_bytes, bytes)
        assert len(output_bytes) > 0

        df_resultado = pd.read_excel(BytesIO(output_bytes))
        assert not df_resultado.empty

        columnas_esperadas = {
            "N\u00b0",
            "NOMBRES Y APELLIDOS",
            "COND.",
            "CARG.",
            "1",
            "2",
        }
        assert columnas_esperadas.issubset(set(df_resultado.columns))
        assert len(df_resultado) == 2  # noqa: PLR2004

    def test_procesar_archivo_con_varias_hojas(self) -> None:
        """Debe procesar multiples hojas y consolidarlas."""
        hojas = [
            [
                ["", "N\u00b0", "NOMBRES", "COND.", "CARG.", "", ""],
                ["", "", "", "", "", "1", "2"],
                ["", "10", "EMPLEADO UNO", "A", "OP", "X", ""],
            ],
            [
                ["", "N\u00b0", "NOMBRES", "COND.", "CARG.", "", ""],
                ["", "", "", "", "", "1", "2"],
                ["", "20", "EMPLEADO DOS", "B", "SUP", "", "X"],
            ],
        ]
        input_bytes = _generar_excel_valido(hojas)
        output_bytes = TurnoService.procesar_archivo(input_bytes)

        excel_io = BytesIO(output_bytes)
        xls = pd.ExcelFile(excel_io)
        total = sum(len(pd.read_excel(excel_io, sheet_name=s)) for s in xls.sheet_names)
        assert total == 2  # noqa: PLR2004

    def test_rechaza_bytes_invalidos(self) -> None:
        """Debe lanzar ValueError con bytes no-Excel."""
        with pytest.raises(ValueError, match="No se pudo leer"):
            TurnoService.procesar_archivo(b"")

    def test_rechaza_sin_cabecera_valida(self) -> None:
        """Debe lanzar ValueError si ninguna hoja tiene cabecera."""
        hojas = [
            [
                ["", "OTRO", "DATOS", "", "", "", ""],
                ["", "1", "ALGO", "A", "OP", "X", ""],
            ],
        ]
        input_bytes = _generar_excel_valido(hojas)

        with pytest.raises(ValueError, match="no contiene datos validos"):
            TurnoService.procesar_archivo(input_bytes)

    def test_columna_id_es_entero(self) -> None:
        """La columna N° debe ser de tipo entero en el resultado."""
        input_bytes = _generar_excel_valido()
        output_bytes = TurnoService.procesar_archivo(input_bytes)

        df_resultado = pd.read_excel(BytesIO(output_bytes))
        assert df_resultado["N\u00b0"].dtype in (int, "int64", "int32")

    def test_nombre_pestana_limitado(self) -> None:
        """El nombre de pestaña debe limitarse a 31 caracteres."""
        hoja_larga = [
            ["", "N\u00b0", "NOMBRES", "COND.", "CARG.", "", ""],
            ["", "", "", "", "", "1"],
            ["", "1", "TEST", "A", "OP", "X"],
        ]
        nombre_largo = "A" * 50

        buffer = BytesIO()
        df = pd.DataFrame(hoja_larga)
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:  # type: ignore[arg-type]
            df.to_excel(writer, index=False, header=False, sheet_name=nombre_largo)
        buffer.seek(0)
        input_bytes = buffer.getvalue()

        output_bytes = TurnoService.procesar_archivo(input_bytes)
        df_resultado = pd.read_excel(
            BytesIO(output_bytes), sheet_name=nombre_largo[:31]
        )
        assert not df_resultado.empty
