"""Tests for Usuario entity."""

from datetime import UTC, datetime
import pytest

from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


def test_create_usuario() -> None:
    """Test creating a usuario."""
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
    assert usuario.id == 1
    assert usuario.nombre == "Juan Pérez"
    assert str(usuario.email) == "test@example.com"
    assert usuario.activo is True


def test_create_usuario_empty_nombre() -> None:
    """Test creating usuario with empty nombre raises error."""
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    with pytest.raises(ValueError, match="Nombre cannot be empty"):
        Usuario(
            id=None,
            nombre="",
            email=email,
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        )


def test_create_usuario_nombre_too_long() -> None:
    """Test creating usuario with nombre too long raises error."""
    email = EmailAddress("test@example.com")
    now = datetime.now(UTC)
    long_nombre = "a" * 256
    with pytest.raises(
        ValueError, match="Nombre cannot exceed 255 characters"
    ):
        Usuario(
            id=None,
            nombre=long_nombre,
            email=email,
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        )


def test_activar_usuario() -> None:
    """Test activating a usuario."""
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
    usuario.activar()
    assert usuario.activo is True


def test_desactivar_usuario() -> None:
    """Test deactivating a usuario."""
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
    usuario.desactivar()
    assert usuario.activo is False


def test_actualizar_nombre() -> None:
    """Test updating usuario nombre."""
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
    usuario.actualizar_nombre("Pedro García")
    assert usuario.nombre == "Pedro García"


def test_actualizar_nombre_empty() -> None:
    """Test updating nombre with empty string raises error."""
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
    with pytest.raises(ValueError, match="Nombre cannot be empty"):
        usuario.actualizar_nombre("")
