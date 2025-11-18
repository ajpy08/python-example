"""Tests for GetUsuarioUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock

from core.application.use_cases.get_usuario_use_case import GetUsuarioUseCase
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


def test_get_usuario_success() -> None:
    """Test successful usuario retrieval."""
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
    mock_repository.get_by_id.return_value = usuario

    use_case = GetUsuarioUseCase(mock_repository)

    # Act
    result = use_case.execute(1)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.nombre == "Juan Pérez"
    assert result.email == "test@example.com"
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_usuario_not_found() -> None:
    """Test getting non-existent usuario returns None."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_by_id.return_value = None

    use_case = GetUsuarioUseCase(mock_repository)

    # Act
    result = use_case.execute(999)

    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
