"""Repositorio para el modelo Empleado."""

from sqlmodel import Session, col, select

from app.models.empleado import Empleado


class EmpleadoRepository:
    """Repositorio para el modelo Empleado."""

    def __init__(self, session: Session) -> None:
        """Inicio."""
        self.session = session

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Empleado]:
        """Obtener todos los empleados con paginacion."""
        stmt = select(Empleado).offset(offset).limit(limit)
        return list(self.session.exec(stmt).all())

    def get_by_id(self, empleado_id: int) -> Empleado | None:
        """Obtener un empleado por su ID."""
        return self.session.get(Empleado, empleado_id)

    def get_by_numero_documento(self, numero_documento: str) -> Empleado | None:
        """Obtener un empleado por su numero de documento.

        Returns:
            El empleado o None si no se encuentra.

        """
        stmt = select(Empleado).where(
            col(Empleado.numero_documento) == numero_documento
        )
        return self.session.exec(stmt).first()

    def search_by_nombre_completo(self, query: str) -> Empleado | None:
        """Buscar un empleado por nombre completo (busqueda parcial, case-insensitive).

        Args:
            query: Fragmento del nombre a buscar.

        Returns:
            El primer empleado encontrado o None.

        """
        stmt = select(Empleado).where(col(Empleado.nombre_completo).ilike(f"%{query}%"))
        return self.session.exec(stmt).first()

    def create(self, empleado: Empleado) -> Empleado:
        """Crear un nuevo empleado."""
        self.session.add(empleado)
        self.session.commit()
        self.session.refresh(empleado)
        return empleado

    def update(self, empleado: Empleado) -> Empleado:
        """Actualizar un empleado existente."""
        self.session.add(empleado)
        self.session.commit()
        self.session.refresh(empleado)
        return empleado

    def delete(self, empleado: Empleado) -> None:
        """Eliminar un empleado."""
        self.session.delete(empleado)
        self.session.commit()
