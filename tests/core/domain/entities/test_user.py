"""Tests for User entity."""

from datetime import UTC, datetime
import pytest

from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress


def test_create_user() -> None:
    """Test creating a user."""
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
    assert user.id == 1
    assert user.name == "John Doe"
    assert str(user.email) == "test@example.com"
    assert user.active is True


def test_create_user_empty_name() -> None:
    """Test creating user with empty name raises error."""
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        User(
            id=None,
            name="",
            email=email,
            active=True,
            created_at=now,
            updated_at=now,
        )


def test_create_user_name_too_long() -> None:
    """Test creating user with name too long raises error."""
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    long_name = "a" * 256
    with pytest.raises(
        ValueError, match="Name cannot exceed 255 characters"
    ):
        User(
            id=None,
            name=long_name,
            email=email,
            active=True,
            created_at=now,
            updated_at=now,
        )


def test_activate_user() -> None:
    """Test activating a user."""
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
    user.activate()
    assert user.active is True


def test_deactivate_user() -> None:
    """Test deactivating a user."""
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
    user.deactivate()
    assert user.active is False


def test_update_name() -> None:
    """Test updating user name."""
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
    user.update_name("Jane Doe")
    assert user.name == "Jane Doe"


def test_update_name_empty() -> None:
    """Test updating name with empty string raises error."""
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
    with pytest.raises(ValueError, match="Name cannot be empty"):
        user.update_name("")
