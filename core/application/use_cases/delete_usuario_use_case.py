"""Delete usuario use case."""

from core.application.ports.usuario_repository_port import (
    UsuarioRepositoryPort,
)


class DeleteUsuarioUseCase:
    """Use case for deleting a usuario."""

    def __init__(self, usuario_repository: UsuarioRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._usuario_repository = usuario_repository

    def execute(self, usuario_id: int) -> bool:
        """Execute the delete usuario use case."""
        return self._usuario_repository.delete(usuario_id)
