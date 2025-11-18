"""Tests for GetUserUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock

from core.application.use_cases.get_user_use_case import GetUserUseCase
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


def test_get_user_success() -> None:
    """Test successful user retrieval."""
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
    mock_repository.get_by_id.return_value = user

    use_case = GetUserUseCase(mock_repository)

    # Act
    result = use_case.execute(1)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.name == "John Doe"
    assert result.email == "test@example.com"
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_user_not_found() -> None:
    """Test getting non-existent user returns None."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = None

    use_case = GetUserUseCase(mock_repository)

    # Act
    result = use_case.execute(999)

    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
