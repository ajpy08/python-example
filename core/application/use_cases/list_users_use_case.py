"""List users use case."""

from typing import List

from core.application.dto.user_dto import UserResponseDto
from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)


class ListUsersUseCase:
    """Use case for listing users."""

    def __init__(self, user_repository: UserRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._user_repository = user_repository

    def execute(
        self, skip: int = 0, limit: int = 100
    ) -> List[UserResponseDto]:
        """Execute the list users use case."""
        users = self._user_repository.get_all(skip=skip, limit=limit)

        return [
            UserResponseDto(
                id=user.id or 0,
                name=user.name,
                email=str(user.email),
                active=user.active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]
