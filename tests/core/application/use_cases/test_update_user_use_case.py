"""Tests for UpdateUserUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock
import pytest

from core.application.dto.user_dto import UpdateUserDto
from core.application.use_cases.update_user_use_case import (
    UpdateUserUseCase,
)
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


def test_update_user_success() -> None:
    """Test successful user update."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    updated_user = User(
        id=1,
        name="John Doe Updated",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.update.return_value = updated_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(name="John Doe Updated")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.name == "John Doe Updated"
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once()


def test_update_user_not_found() -> None:
    """Test updating non-existent user returns None."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = None

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(name="John Doe Updated")

    # Act
    result = use_case.execute(999, dto)

    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.update.assert_not_called()


def test_update_user_email() -> None:
    """Test updating user email."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    updated_user = User(
        id=1,
        name="John Doe",
        email=EmailAddress("new@example.com"),
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = updated_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(email="new@example.com")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.email == "new@example.com"
    mock_repository.get_by_email.assert_called_once_with("new@example.com")


def test_update_user_email_already_exists() -> None:
    """Test updating user with existing email raises error."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    existing_user = User(
        id=2,  # Different ID
        name="Other User",
        email=EmailAddress("new@example.com"),
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.get_by_email.return_value = existing_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(email="new@example.com")

    # Act & Assert
    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(1, dto)

    mock_repository.get_by_email.assert_called_once_with("new@example.com")
    mock_repository.update.assert_not_called()


def test_update_user_email_same_user() -> None:
    """Test updating user with same email (same user) is allowed."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    updated_user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.get_by_email.return_value = user  # Same user
    mock_repository.update.return_value = updated_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(email="test@example.com")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    mock_repository.update.assert_called_once()


def test_update_user_active() -> None:
    """Test updating user active status."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    updated_user = User(
        id=1,
        name="John Doe",
        email=email,
        active=False,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.update.return_value = updated_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(active=False)

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.active is False
    mock_repository.update.assert_called_once()


def test_update_user_multiple_fields() -> None:
    """Test updating multiple user fields at once."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    updated_user = User(
        id=1,
        name="John Doe Updated",
        email=EmailAddress("new@example.com"),
        active=False,
        created_at=now,
        updated_at=now,
    )
    mock_repository.get_by_id.return_value = user
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = updated_user

    use_case = UpdateUserUseCase(mock_repository)
    dto = UpdateUserDto(
        name="John Doe Updated",
        email="new@example.com",
        active=False,
    )

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.name == "John Doe Updated"
    assert result.email == "new@example.com"
    assert result.active is False
