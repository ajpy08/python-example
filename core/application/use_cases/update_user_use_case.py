"""Update user use case."""

from typing import Optional

from core.application.dto.user_dto import (
    UpdateUserDto,
    UserResponseDto,
)
from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)
from core.domain.value_objects.email_address import EmailAddress


class UpdateUserUseCase:
    """Use case for updating a user."""

    def __init__(self, user_repository: UserRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._user_repository = user_repository

    def execute(
        self, user_id: int, dto: UpdateUserDto
    ) -> Optional[UserResponseDto]:
        """Execute the update user use case."""
        user = self._user_repository.get_by_id(user_id)
        if not user:
            return None

        # Update fields if provided
        if dto.name is not None:
            user.update_name(dto.name)

        if dto.email is not None:
            # Check if new email already exists
            existing_user = self._user_repository.get_by_email(dto.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(
                    f"User with email {dto.email} already exists"
                )
            user.email = EmailAddress(dto.email)

        if dto.active is not None:
            if dto.active:
                user.activate()
            else:
                user.deactivate()

        # Save via repository
        updated_user = self._user_repository.update(user)

        # Map to response DTO
        return UserResponseDto(
            id=updated_user.id or 0,
            name=updated_user.name,
            email=str(updated_user.email),
            active=updated_user.active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )
