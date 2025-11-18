"""List usuarios use case."""

from typing import List

from core.application.dto.usuario_dto import UsuarioResponseDto
from core.application.ports.usuario_repository_port import (
    UsuarioRepositoryPort,
)


class ListUsuariosUseCase:
    """Use case for listing usuarios."""

    def __init__(self, usuario_repository: UsuarioRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._usuario_repository = usuario_repository

    def execute(
        self, skip: int = 0, limit: int = 100
    ) -> List[UsuarioResponseDto]:
        """Execute the list usuarios use case."""
        usuarios = self._usuario_repository.get_all(skip=skip, limit=limit)

        return [
            UsuarioResponseDto(
                id=usuario.id or 0,
                nombre=usuario.nombre,
                email=str(usuario.email),
                activo=usuario.activo,
                fecha_creacion=usuario.fecha_creacion,
                fecha_actualizacion=usuario.fecha_actualizacion,
            )
            for usuario in usuarios
        ]
