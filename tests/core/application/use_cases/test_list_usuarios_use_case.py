"""Tests for ListUsuariosUseCase."""

from datetime import UTC, datetime
from unittest.mock import Mock

from core.application.use_cases.list_usuarios_use_case import (
    ListUsuariosUseCase,
)
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress


def test_list_usuarios_success() -> None:
    """Test successful usuario listing."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    usuarios = [
        Usuario(
            id=1,
            nombre="Juan Pérez",
            email=EmailAddress("juan@example.com"),
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        ),
        Usuario(
            id=2,
            nombre="María García",
            email=EmailAddress("maria@example.com"),
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        ),
    ]
    mock_repository.get_all.return_value = usuarios

    use_case = ListUsuariosUseCase(mock_repository)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].nombre == "Juan Pérez"
    assert result[0].email == "juan@example.com"
    assert result[1].id == 2
    assert result[1].nombre == "María García"
    assert result[1].email == "maria@example.com"
    mock_repository.get_all.assert_called_once_with(skip=0, limit=100)


def test_list_usuarios_with_pagination() -> None:
    """Test listing usuarios with pagination parameters."""
    # Arrange
    mock_repository = Mock()
    now = datetime.now(UTC)
    usuarios = [
        Usuario(
            id=1,
            nombre="Juan Pérez",
            email=EmailAddress("juan@example.com"),
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        ),
    ]
    mock_repository.get_all.return_value = usuarios

    use_case = ListUsuariosUseCase(mock_repository)

    # Act
    result = use_case.execute(skip=10, limit=5)

    # Assert
    assert len(result) == 1
    mock_repository.get_all.assert_called_once_with(skip=10, limit=5)


def test_list_usuarios_empty() -> None:
    """Test listing usuarios when repository returns empty list."""
    # Arrange
    mock_repository = Mock()
    mock_repository.get_all.return_value = []

    use_case = ListUsuariosUseCase(mock_repository)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 0
    assert result == []
    mock_repository.get_all.assert_called_once_with(skip=0, limit=100)

