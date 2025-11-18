"""Tests for ListUsersUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock

from core.application.use_cases.list_users_use_case import (
    ListUsersUseCase,
)
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


def test_list_users_success() -> None:
    """Test successful user listing."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    users = [
        User(
            id=1,
            name="John Doe",
            email=EmailAddress("juan@example.com"),
            active=True,
            created_at=now,
            updated_at=now,
        ),
        User(
            id=2,
            name="Jane Doe",
            email=EmailAddress("maria@example.com"),
            active=True,
            created_at=now,
            updated_at=now,
        ),
    ]
    mock_repository.get_all.return_value = users

    use_case = ListUsersUseCase(mock_repository)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "John Doe"
    assert result[0].email == "juan@example.com"
    assert result[1].id == 2
    assert result[1].name == "Jane Doe"
    assert result[1].email == "maria@example.com"
    mock_repository.get_all.assert_called_once_with(skip=0, limit=100)


def test_list_users_with_pagination() -> None:
    """Test listing users with pagination parameters."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    users = [
        User(
            id=1,
            name="John Doe",
            email=EmailAddress("juan@example.com"),
            active=True,
            created_at=now,
            updated_at=now,
        ),
    ]
    mock_repository.get_all.return_value = users

    use_case = ListUsersUseCase(mock_repository)

    # Act
    result = use_case.execute(skip=10, limit=5)

    # Assert
    assert len(result) == 1
    mock_repository.get_all.assert_called_once_with(skip=10, limit=5)


def test_list_users_empty() -> None:
    """Test listing users when repository returns empty list."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_all.return_value = []

    use_case = ListUsersUseCase(mock_repository)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 0
    assert result == []
    mock_repository.get_all.assert_called_once_with(skip=0, limit=100)
