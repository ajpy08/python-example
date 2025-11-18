"""Tests for UsuarioDomainService."""

from datetime import UTC, datetime
import pytest

from core.domain.entities.usuario import Usuario
from core.domain.services.usuario_domain_service import UsuarioDomainService
from core.domain.value_objects.email_address import EmailAddress


def test_puede_activar_usuario_when_inactive() -> None:
    """Test puede_activar_usuario returns True when usuario is inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=False,  # Usuario inactivo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    result = UsuarioDomainService.puede_activar_usuario(usuario)

    # Assert
    assert result is True


def test_puede_activar_usuario_when_active() -> None:
    """Test puede_activar_usuario returns False when usuario is already active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,  # Usuario ya activo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    result = UsuarioDomainService.puede_activar_usuario(usuario)

    # Assert
    assert result is False


def test_puede_desactivar_usuario_when_active() -> None:
    """Test puede_desactivar_usuario returns True when usuario is active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,  # Usuario activo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    result = UsuarioDomainService.puede_desactivar_usuario(usuario)

    # Assert
    assert result is True


def test_puede_desactivar_usuario_when_inactive() -> None:
    """Test puede_desactivar_usuario returns False when usuario is already inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=False,  # Usuario ya inactivo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    result = UsuarioDomainService.puede_desactivar_usuario(usuario)

    # Assert
    assert result is False


def test_activar_usuario_uses_domain_service() -> None:
    """Test that activar() method uses domain service validation."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=False,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    usuario.activar()

    # Assert
    assert usuario.activo is True


def test_activar_usuario_already_active_raises_error() -> None:
    """Test that activar() raises error when usuario is already active."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,  # Ya está activo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Usuario ya está activo"):
        usuario.activar()


def test_desactivar_usuario_uses_domain_service() -> None:
    """Test that desactivar() method uses domain service validation."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    usuario.desactivar()

    # Assert
    assert usuario.activo is False


def test_desactivar_usuario_already_inactive_raises_error() -> None:
    """Test that desactivar() raises error when usuario is already inactive."""
    # Arrange
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=False,  # Ya está inactivo
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Usuario ya está inactivo"):
        usuario.desactivar()

