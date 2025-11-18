"""Tests for UserDomainService."""

from datetime import UTC, datetime
import pytest

from core.domain.entities.user import User
from core.domain.services.user_domain_service import UserDomainService
from core.domain.value_objects.email_address import EmailAddress


def test_can_activate_user_when_inactive() -> None:
    """Test can_activate_user returns True when user is inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=False,  # User inactive
        created_at=now,
        updated_at=now,
    )

    # Act
    result = UserDomainService.can_activate_user(user)

    # Assert
    assert result is True


def test_can_activate_user_when_active() -> None:
    """Test can_activate_user returns False when user is already active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,  # User already active
        created_at=now,
        updated_at=now,
    )

    # Act
    result = UserDomainService.can_activate_user(user)

    # Assert
    assert result is False


def test_can_deactivate_user_when_active() -> None:
    """Test can_deactivate_user returns True when user is active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,  # User active
        created_at=now,
        updated_at=now,
    )

    # Act
    result = UserDomainService.can_deactivate_user(user)

    # Assert
    assert result is True


def test_can_deactivate_user_when_inactive() -> None:
    """Test can_deactivate_user returns False when user is already inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=False,  # User already inactive
        created_at=now,
        updated_at=now,
    )

    # Act
    result = UserDomainService.can_deactivate_user(user)

    # Assert
    assert result is False


def test_activate_user_uses_domain_service() -> None:
    """Test that activate() method uses domain service validation."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=False,
        created_at=now,
        updated_at=now,
    )

    # Act
    user.activate()

    # Assert
    assert user.active is True


def test_activate_user_already_active_raises_error() -> None:
    """Test that activate() raises error when user is already active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,  # Already active
        created_at=now,
        updated_at=now,
    )

    # Act & Assert
    with pytest.raises(ValueError, match="User is already active"):
        user.activate()


def test_deactivate_user_uses_domain_service() -> None:
    """Test that deactivate() method uses domain service validation."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )

    # Act
    user.deactivate()

    # Assert
    assert user.active is False


def test_deactivate_user_already_inactive_raises_error() -> None:
    """Test that deactivate() raises error when user is already inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    user = User(
        id=1,
        name="John Doe",
        email=email,
        active=False,  # Already inactive
        created_at=now,
        updated_at=now,
    )

    # Act & Assert
    with pytest.raises(ValueError, match="User is already inactive"):
        user.deactivate()
