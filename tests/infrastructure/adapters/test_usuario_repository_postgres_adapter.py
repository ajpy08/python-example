"""Tests for UsuarioRepositoryPostgresAdapter."""

from datetime import UTC, datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress
from infrastructure.adapters.repositories.usuario_repository_postgres_adapter import (  # noqa: E501
    UsuarioRepositoryPostgresAdapter,
)
from infrastructure.database.models.usuario_model import Base


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine, autocommit=False, autoflush=False
    )
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_create_usuario(db_session) -> None:
    """Test creating a usuario."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=None,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )

    # Act
    result = adapter.create(usuario)

    # Assert
    assert result.id is not None
    assert result.nombre == "Juan Pérez"
    assert str(result.email) == "test@example.com"
    assert result.activo is True


def test_get_by_id(db_session) -> None:
    """Test getting usuario by id."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=None,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    created = adapter.create(usuario)

    # Act
    result = adapter.get_by_id(created.id or 0)

    # Assert
    assert result is not None
    assert result.id == created.id
    assert result.nombre == "Juan Pérez"


def test_get_by_id_not_found(db_session) -> None:
    """Test getting non-existent usuario returns None."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)

    # Act
    result = adapter.get_by_id(999)

    # Assert
    assert result is None


def test_get_by_email(db_session) -> None:
    """Test getting usuario by email."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=None,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    adapter.create(usuario)

    # Act
    result = adapter.get_by_email("test@example.com")

    # Assert
    assert result is not None
    assert str(result.email) == "test@example.com"


def test_get_all(db_session) -> None:
    """Test getting all usuarios."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)

    for i in range(3):
        email = EmailAddress(f"test{i}@example.com")
        usuario = Usuario(
            id=None,
            nombre=f"Usuario {i}",
            email=email,
            activo=True,
            fecha_creacion=now,
            fecha_actualizacion=now,
        )
        adapter.create(usuario)

    # Act
    results = adapter.get_all()

    # Assert
    assert len(results) == 3


def test_update_usuario(db_session) -> None:
    """Test updating a usuario."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=None,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    created = adapter.create(usuario)
    created.actualizar_nombre("Pedro García")

    # Act
    result = adapter.update(created)

    # Assert
    assert result.nombre == "Pedro García"


def test_delete_usuario(db_session) -> None:
    """Test deleting a usuario."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    usuario = Usuario(
        id=None,
        nombre="Juan Pérez",
        email=email,
        activo=True,
        fecha_creacion=now,
        fecha_actualizacion=now,
    )
    created = adapter.create(usuario)

    # Act
    result = adapter.delete(created.id or 0)

    # Assert
    assert result is True
    assert adapter.get_by_id(created.id or 0) is None


def test_delete_usuario_not_found(db_session) -> None:
    """Test deleting non-existent usuario returns False."""
    # Arrange
    adapter = UsuarioRepositoryPostgresAdapter(db_session)

    # Act
    result = adapter.delete(999)

    # Assert
    assert result is False
