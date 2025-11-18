"""Update usuario use case."""

from typing import Optional

from core.application.dto.usuario_dto import UpdateUsuarioDto, UsuarioResponseDto
from core.application.ports.usuario_repository_port import UsuarioRepositoryPort
from core.domain.value_objects.email_address import EmailAddress


class UpdateUsuarioUseCase:
    """Use case for updating a usuario."""

    def __init__(self, usuario_repository: UsuarioRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._usuario_repository = usuario_repository

    def execute(
        self, usuario_id: int, dto: UpdateUsuarioDto
    ) -> Optional[UsuarioResponseDto]:
        """Execute the update usuario use case."""
        usuario = self._usuario_repository.get_by_id(usuario_id)
        if not usuario:
            return None

        # Update fields if provided
        if dto.nombre is not None:
            usuario.actualizar_nombre(dto.nombre)

        if dto.email is not None:
            # Check if new email already exists
            existing_usuario = self._usuario_repository.get_by_email(dto.email)
            if existing_usuario and existing_usuario.id != usuario_id:
                raise ValueError(f"Usuario with email {dto.email} already exists")
            usuario.email = EmailAddress(dto.email)

        if dto.activo is not None:
            if dto.activo:
                usuario.activar()
            else:
                usuario.desactivar()

        # Save via repository
        updated_usuario = self._usuario_repository.update(usuario)

        # Map to response DTO
        return UsuarioResponseDto(
            id=updated_usuario.id or 0,
            nombre=updated_usuario.nombre,
            email=str(updated_usuario.email),
            activo=updated_usuario.activo,
            fecha_creacion=updated_usuario.fecha_creacion,
            fecha_actualizacion=updated_usuario.fecha_actualizacion,
        )

