"""User repository port."""

from typing import List, Optional, Protocol

from core.domain.entities.user import User


class UserRepositoryPort(Protocol):
    """Port for user repository operations."""

    def create(self, user: User) -> User:
        """Create a new user."""
        ...

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id."""
        ...

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        ...

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        ...

    def update(self, user: User) -> User:
        """Update an existing user."""
        ...

    def delete(self, user_id: int) -> bool:
        """Delete a user by id."""
        ...
