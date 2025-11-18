"""Tests for EmailAddress value object."""

import pytest

from core.domain.value_objects.email_address import EmailAddress


def test_create_valid_email() -> None:
    """Test creating a valid email address."""
    email = EmailAddress("test@example.com")
    assert str(email) == "test@example.com"
    assert email.value == "test@example.com"


def test_create_invalid_email_empty() -> None:
    """Test creating email with empty string raises error."""
    with pytest.raises(ValueError, match="Email cannot be empty"):
        EmailAddress("")


def test_create_invalid_email_format() -> None:
    """Test creating email with invalid format raises error."""
    with pytest.raises(ValueError, match="Invalid email format"):
        EmailAddress("invalid-email")


def test_create_invalid_email_no_at() -> None:
    """Test creating email without @ raises error."""
    with pytest.raises(ValueError, match="Invalid email format"):
        EmailAddress("invalidemail.com")


def test_email_immutability() -> None:
    """Test that EmailAddress is immutable."""
    email = EmailAddress("test@example.com")
    # Should be frozen dataclass
    with pytest.raises(Exception):
        email.value = "new@example.com"

