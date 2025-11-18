"""Tests for UpdateUsuarioUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock
import pytest

from core.application.dto.usuario_dto import UpdateUsuarioDto
from core.application.use_cases.update_usuario_use_case import (
    UpdateUsuarioUseCase,
)
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


def test_update_usuario_success() -> None:
    """Test successful usuario update."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    updated_usuario = Usuario(
        id=1,
        nombre="Juan Pérez Actualizado",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.update.return_value = updated_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(nombre="Juan Pérez Actualizado")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.nombre == "Juan Pérez Actualizado"
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once()


def test_update_usuario_not_found() -> None:
    """Test updating non-existent usuario returns None."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = None

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(nombre="Juan Pérez Actualizado")

    # Act
    result = use_case.execute(999, dto)

    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.update.assert_not_called()


def test_update_usuario_email() -> None:
    """Test updating usuario email."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    updated_usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=EmailAddress("nuevo@example.com"),
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = updated_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(email="nuevo@example.com")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.email == "nuevo@example.com"
    mock_repository.get_by_email.assert_called_once_with("nuevo@example.com")


def test_update_usuario_email_already_exists() -> None:
    """Test updating usuario with existing email raises error."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    existing_usuario = Usuario(
        id=2,  # Diferente ID
        nombre="Otro Usuario",
        email=EmailAddress("nuevo@example.com"),
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.get_by_email.return_value = existing_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(email="nuevo@example.com")

    # Act & Assert
    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(1, dto)

    mock_repository.get_by_email.assert_called_once_with("nuevo@example.com")
    mock_repository.update.assert_not_called()


def test_update_usuario_email_same_user() -> None:
    """Test updating usuario with same email (same user) is allowed."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    updated_usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.get_by_email.return_value = usuario  # Mismo usuario
    mock_repository.update.return_value = updated_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(email="test@example.com")

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    mock_repository.update.assert_called_once()


def test_update_usuario_activo() -> None:
    """Test updating usuario activo status."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    updated_usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=False,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.update.return_value = updated_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(activo=False)

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.activo is False
    mock_repository.update.assert_called_once()


def test_update_usuario_multiple_fields() -> None:
    """Test updating multiple usuario fields at once."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    updated_usuario = Usuario(
        id=1,
        nombre="Juan Pérez Actualizado",
        email=EmailAddress("nuevo@example.com"),
        activo=False,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_id.return_value = usuario
    mock_repository.get_by_email.return_value = None
    mock_repository.update.return_value = updated_usuario

    use_case = UpdateUsuarioUseCase(mock_repository)
    dto = UpdateUsuarioDto(
        nombre="Juan Pérez Actualizado",
        email="nuevo@example.com",
        activo=False,
    )

    # Act
    result = use_case.execute(1, dto)

    # Assert
    assert result is not None
    assert result.nombre == "Juan Pérez Actualizado"
    assert result.email == "nuevo@example.com"
    assert result.activo is False

