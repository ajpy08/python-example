"""Tests for CreateUsuarioUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock
import pytest

from core.application.dto.usuario_dto import CreateUsuarioDto
from core.application.use_cases.create_usuario_use_case import (
    CreateUsuarioUseCase,
)
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


def test_create_usuario_success() -> None:
    """Test successful usuario creation."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    created_usuario = Usuario(
        id=1,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = created_usuario

    use_case = CreateUsuarioUseCase(mock_repository)
    dto = CreateUsuarioDto(
        nombre="Juan Pérez", email="test@example.com", activo=True
    )

    # Act
    result = use_case.execute(dto)

    # Assert
    assert result.id == 1
    assert result.nombre == "Juan Pérez"
    assert result.email == "test@example.com"
    assert result.activo is True
    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.create.assert_called_once()


def test_create_usuario_email_already_exists() -> None:
    """Test creating usuario with existing email raises error."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    existing_usuario = Usuario(
        id=1,
        nombre="Existing User",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    mock_repository.get_by_email.return_value = existing_usuario

    use_case = CreateUsuarioUseCase(mock_repository)
    dto = CreateUsuarioDto(
        nombre="Juan Pérez", email="test@example.com", activo=True
    )

    # Act & Assert
    with pytest.raises(ValueError, match="already exists"):
        use_case.execute(dto)

    mock_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_repository.create.assert_not_called()
