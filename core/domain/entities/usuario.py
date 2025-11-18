"""Usuario entity."""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Optional

from core.domain.value_objects.email_address import EmailAddress


@dataclass
class Usuario:
    """Usuario domain entity."""

    id: Optional[int]
    nombre: str
    email: EmailAddress
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("Nombre cannot be empty")
        if len(self.nombre) > 255:
            raise ValueError("Nombre cannot exceed 255 characters")

    def activar(self) -> None:
        """Activate the usuario."""
        self.activo = True
        self.fecha_actualizacion = datetime.now(UTC)

    def desactivar(self) -> None:
        """Deactivate the usuario."""
        self.activo = False
        self.fecha_actualizacion = datetime.now(UTC)

    def actualizar_nombre(self, nuevo_nombre: str) -> None:
        """Update usuario name."""
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("Nombre cannot be empty")
        if len(nuevo_nombre) > 255:
            raise ValueError("Nombre cannot exceed 255 characters")
        self.nombre = nuevo_nombre.strip()
        self.fecha_actualizacion = datetime.now(UTC)

