"""Tests for CreateUserUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock
import pytest

from core.application.dto.user_dto import CreateUserDto
from core.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


def test_create_user_success() -> None:
    """Test successful user creation."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    created_user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = created_user

    use_case = CreateUserUseCase(mock_repository)
    dto = CreateUserDto(
        name="John Doe", email="test@example.com", active=True
    )

    # Act
    result = use_case.execute(dto)

    # Assert
    assert result.id == 1
    assert result.name == "John Doe"
    assert result.email == "test@example.com"
    assert result.active is True
    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.create.assert_called_once()


def test_create_user_email_already_exists() -> None:
    """Test creating user with existing email raises error."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    existing_user = User(
        id=1,
        name="Existing User",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_email.return_value = existing_user

    use_case = CreateUserUseCase(mock_repository)
    dto = CreateUserDto(
        name="John Doe", email="test@example.com", active=True
    )

    # Act & Assert
    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(dto)

    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.create.assert_not_called()
