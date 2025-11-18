"""Create usuario use case."""

from datetime import UTC, datetime

from core.application.dto.usuario_dto import CreateUsuarioDto, UsuarioResponseDto
from core.application.ports.usuario_repository_port import UsuarioRepositoryPort
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


class CreateUsuarioUseCase:
    """Use case for creating a usuario."""

    def __init__(self, usuario_repository: UsuarioRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._usuario_repository = usuario_repository

    def execute(self, dto: CreateUsuarioDto) -> UsuarioResponseDto:
        """Execute the create usuario use case."""
        # Check if email already exists
        existing_usuario = self._usuario_repository.get_by_email(dto.email)
        if existing_usuario:
            raise ValueError(f"Usuario with email {dto.email} already exists")

        # Create domain entity
        email = EmailAddress(dto.email)
        now = datetime.now(UTC)
        usuario = Usuario(
            id=None,
            nombre=dto.nombre,
            email=email,
            activo=dto.activo,
            fecha_creacion=now,
            fecha_actualizacion=now,
        )

        # Save via repository
        created_usuario = self._usuario_repository.create(usuario)

        # Map to response DTO
        return UsuarioResponseDto(
            id=created_usuario.id or 0,
            nombre=created_usuario.nombre,
            email=str(created_usuario.email),
            activo=created_usuario.activo,
            fecha_creacion=created_usuario.fecha_creacion,
            fecha_actualizacion=created_usuario.fecha_actualizacion,
        )

