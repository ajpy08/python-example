"""Delete user use case."""

from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)


class DeleteUserUseCase:
    """Use case for deleting a user."""

    def __init__(self, user_repository: UserRepositoryPort) -> None:
        """Initialize use case with repository port."""
        self._user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        """Execute the delete user use case."""
        return self._user_repository.delete(user_id)
