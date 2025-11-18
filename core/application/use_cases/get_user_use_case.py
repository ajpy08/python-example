"""Get user use case."""

from typing import Optional

from core.application.dto.user_dto import UserResponseDto
from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)


class GetUserUseCase:
    """Use case for getting a user by id."""

    def __init__(self, user_repository: UserRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._user_repository = user_repository

    def execute(self, user_id: int) -> Optional[UserResponseDto]:
        """Execute the get user use case."""
        user = self._user_repository.get_by_id(user_id)
        if not user:
            return None

        return UserResponseDto(
            id=user.id or 0,
            name=user.name,
            email=str(user.email),
            active=user.active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
