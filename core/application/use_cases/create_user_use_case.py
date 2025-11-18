"""Create user use case."""

from datetime import UTC, datetime

from core.application.dto.user_dto import (
    CreateUserDto,
    UserResponseDto,
)
from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


class CreateUserUseCase:
    """Use case for creating a user."""

    def __init__(self, user_repository: UserRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._user_repository = user_repository

    def execute(self, dto: CreateUserDto) -> UserResponseDto:
        """Execute the create user use case."""
        # Check if email already exists
        existing_user = self._user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError(f"User with email {dto.email} already exists")

        # Create domain entity
        email = EmailAddress(dto.email)
        now = datetime.now(UTC)
        user = User(
            id=None,
            name=dto.name,
            email=email,
            active=dto.active,
            created_at=now,
            updated_at=now,
        )

        # Save via repository
        created_user = self._user_repository.create(user)

        # Map to response DTO
        return UserResponseDto(
            id=created_user.id or 0,
            name=created_user.name,
            email=str(created_user.email),
            active=created_user.active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )
