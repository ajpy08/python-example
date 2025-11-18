"""Get usuario use case."""

from typing import Optional

from core.application.dto.usuario_dto import UsuarioResponseDto
from core.application.ports.usuario_repository_port import UsuarioRepositoryPort


class GetUsuarioUseCase:
    """Use case for getting a usuario by id."""

    def __init__(self, usuario_repository: UsuarioRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._usuario_repository = usuario_repository

    def execute(self, usuario_id: int) -> Optional[UsuarioResponseDto]:
        """Execute the get usuario use case."""
        usuario = self._usuario_repository.get_by_id(usuario_id)
        if not usuario:
            return None

        return UsuarioResponseDto(
            id=usuario.id or 0,
            nombre=usuario.nombre,
            email=str(usuario.email),
            activo=usuario.activo,
            fecha_creacion=usuario.fecha_creacion,
            fecha_actualizacion=usuario.fecha_actualizacion,
        )

