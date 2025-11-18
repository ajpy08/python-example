"""Usuario DTOs."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateUsuarioDto:
    """DTO for creating a usuario."""

    nombre: str
    email: str
    activo: bool = True


@dataclass
class UpdateUsuarioDto:
    """DTO for updating a usuario."""

    nombre: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = None


@dataclass
class UsuarioResponseDto:
    """DTO for usuario response."""

    id: int
    nombre: str
    email: str
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

