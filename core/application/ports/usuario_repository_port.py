"""Usuario repository port."""

from typing import List, Optional, Protocol

from core.domain.entities.usuario import Usuario


class UsuarioRepositoryPort(Protocol):
    """Port for usuario repository operations."""

    def create(self, usuario: Usuario) -> Usuario:
        """Create a new usuario."""
        ...

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Get usuario by id."""
        ...

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Get usuario by email."""
        ...

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Get all usuarios with pagination."""
        ...

    def update(self, usuario: Usuario) -> Usuario:
        """Update an existing usuario."""
        ...

    def delete(self, usuario_id: int) -> bool:
        """Delete a usuario by id."""
        ...

