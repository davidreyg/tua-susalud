"""Servicio para generar datos TUA desde archivo Excel de input."""

import math
from typing import Any

from sqlmodel import Session

from app.api.responses.tua_input_response import TuaInputDataResponse, TurnoItem
from app.models.empleado import Empleado
from app.repositories.empleado import EmpleadoRepository
from app.repositories.leyenda import LeyendaRepository
from app.services.excel_sheet_service import ExcelSheetService
from tools.logger import Logger

logger = Logger(__name__)

CODIGO_UNICO = "00005883"
NOMBRE_ESTABLECIMIENTO = "HOSPITAL DE HUAYCAN"
RED = "00"


class GenerarDataTuaService:
    """Servicio para generar datos de entrada TUA desde un Excel.

    Lee los registros de un archivo Excel de input, busca cada nombre
    en la base de datos de empleados y construye registros TUA
    consolidados.
    """

    @staticmethod
    def procesar(
        input_bytes: bytes,
        nombre_hoja: str,
        nombre_archivo: str,
        session: Session,
    ) -> dict[str, Any]:
        """Procesa el archivo Excel y genera datos TUA.

        Reutiliza ``ExcelSheetService.obtener_hoja`` para la lectura
        de la hoja y luego enriquece cada registro con datos del empleado.

        Args:
            input_bytes: Contenido binario del archivo Excel.
            nombre_hoja: Nombre de la hoja o indice 1-based.
            nombre_archivo: Nombre original del archivo para logs.
            session: Sesion de base de datos para buscar empleados.

        Returns:
            Diccionario con ``datos`` (lista de TuaInputDataResponse),
            ``total_registros``, ``empleados_encontrados`` y
            ``empleados_no_encontrados`` (lista de nombres).

        Raises:
            ValueError: Si la hoja no existe o el archivo no se puede leer.

        """
        logger.info(
            "Iniciando procesamiento de '%s' hoja '%s'...",
            nombre_archivo,
            nombre_hoja,
        )

        try:
            resultado_excel = ExcelSheetService.obtener_hoja(
                input_bytes=input_bytes,
                hoja=nombre_hoja,
                nombre_archivo=nombre_archivo,
            )
        except ValueError as exc:
            logger.exception("No se pudo leer el archivo")
            msg = f"Error al leer el archivo '{nombre_archivo}': {exc}"
            raise ValueError(msg) from exc
        except Exception as exc:
            logger.exception("Error inesperado al leer el excel")
            msg = f"Error al leer el archivo '{nombre_archivo}': {exc}"
            raise ValueError(msg) from exc

        registros: list[dict[str, Any]] = resultado_excel["datos"]
        empleado_repo = EmpleadoRepository(session)

        datos: list[TuaInputDataResponse] = []
        no_encontrados: list[str] = []

        try:
            for row in registros:
                nombre_completo = str(row.get("NOMBRES Y APELLIDOS", "")).strip()

                if not nombre_completo:
                    logger.debug("Fila sin nombre completo, omitiendo.")
                    continue

                empleado = empleado_repo.search_by_nombre_completo(nombre_completo)

                if empleado:
                    tua_record = GenerarDataTuaService._construir_tua_record(
                        empleado, row, session
                    )
                    datos.append(tua_record)
                    logger.debug(
                        "Empleado encontrado: '%s' (%s)",
                        empleado.nombre_completo,
                        empleado.numero_documento,
                    )
                else:
                    no_encontrados.append(nombre_completo)
                    logger.warning("Empleado NO encontrado: '%s'", nombre_completo)

        except Exception as exc:
            logger.exception("Error durante el procesamiento de registros")
            msg = f"Error procesando registros de '{nombre_archivo}': {exc}"
            raise ValueError(msg) from exc

        logger.info(
            "Procesamiento completado. Encontrados: %d, No encontrados: %d",
            len(datos),
            len(no_encontrados),
        )

        return {
            "datos": [d.model_dump() for d in datos],
            "total_registros": len(registros),
            "empleados_encontrados": len(datos),
            "empleados_no_encontrados": len(no_encontrados),
            "nombres_no_encontrados": no_encontrados,
        }

    @staticmethod
    def _construir_tua_record(
        empleado: Empleado,
        row: dict[str, Any],
        session: Session,
    ) -> TuaInputDataResponse:
        """Construye un registro TUA a partir de un empleado.

        Args:
            empleado: Instancia de Empleado encontrada en la BD.
            row: Fila del Excel con los datos de turnos por dia.
            session: Sesion de base de datos para consultas.

        Returns:
            Registro TUA tipado.

        """
        turnos: list[TurnoItem] = []
        leyenda_repo = LeyendaRepository(session)

        for day in range(1, 32):
            raw = row.get(str(day))

            denominacion = ""
            if raw is not None and not (isinstance(raw, float) and math.isnan(raw)):
                denominacion = str(raw).strip()

            cargo = str(row.get("CARG.", "")).strip()

            if denominacion:
                leyenda = leyenda_repo.get_by_sigla(denominacion, cargo)
                if leyenda:
                    turnos.append(
                        TurnoItem(
                            dia=day,
                            hora_entrada=leyenda.hora_inicio,
                            hora_salida=leyenda.hora_fin,
                        )
                    )
                else:
                    turnos.append(TurnoItem(dia=day))
            else:
                turnos.append(TurnoItem(dia=day))

        return TuaInputDataResponse(
            codigo_unico=CODIGO_UNICO,
            nombre_establecimiento=NOMBRE_ESTABLECIMIENTO,
            red=RED,
            tipo_documento=empleado.tipo_documento,
            numero_documento=empleado.numero_documento,
            profesion=empleado.profesion,
            numero_colegiatura=empleado.numero_de_colegiatura,
            apellidos=empleado.apellidos,
            nombres=empleado.nombres,
            especialidad=empleado.especialidad,
            servicio=empleado.servicio,
            turnos=turnos,
        )
