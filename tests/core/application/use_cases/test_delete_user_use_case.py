"""Tests for DeleteUserUseCase."""

from unittest.mock import Mock

from core.application.use_cases.delete_user_use_case import (
    DeleteUserUseCase,
)


def test_delete_user_success() -> None:
    """Test successful user deletion."""
    # Arrange
    mock_repository = Mock()
    mock_repository.delete.return_value = True

    use_case = DeleteUserUseCase(mock_repository)

    # Act
    result = use_case.execute(1)

    # Assert
    assert result is True
    mock_repository.delete.assert_called_once_with(1)


def test_delete_user_not_found() -> None:
    """Test deleting non-existent user returns False."""
    # Arrange
    mock_repository = Mock()
    mock_repository.delete.return_value = False

    use_case = DeleteUserUseCase(mock_repository)

    # Act
    result = use_case.execute(999)

    # Assert
    assert result is False
    mock_repository.delete.assert_called_once_with(999)
