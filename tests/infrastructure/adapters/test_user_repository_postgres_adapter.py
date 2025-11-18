"""Tests for UserRepositoryPostgresAdapter."""

from datetime import UTC, datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress
from infrastructure.adapters.repositories.user_repository_postgres_adapter import (  # noqa: E501
    UserRepositoryPostgresAdapter,
)
from infrastructure.database.models.user_model import Base


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


def test_create_user(db_session) -> None:
    """Test creating a user."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=None,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )

    # Act
    result = adapter.create(user)

    # Assert
    assert result.id is not None
    assert result.name == "John Doe"
    assert str(result.email) == "test@example.com"
    assert result.active is True


def test_get_by_id(db_session) -> None:
    """Test getting user by id."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=None,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    created = adapter.create(user)

    # Act
    result = adapter.get_by_id(created.id or 0)

    # Assert
    assert result is not None
    assert result.id == created.id
    assert result.name == "John Doe"


def test_get_by_id_not_found(db_session) -> None:
    """Test getting non-existent user returns None."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)

    # Act
    result = adapter.get_by_id(999)

    # Assert
    assert result is None


def test_get_by_email(db_session) -> None:
    """Test getting user by email."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=None,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    adapter.create(user)

    # Act
    result = adapter.get_by_email("test@example.com")

    # Assert
    assert result is not None
    assert str(result.email) == "test@example.com"


def test_get_all(db_session) -> None:
    """Test getting all users."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)

    for i in range(3):
        email = EmailAddress(f"test{i}@example.com")
        user = User(
            id=None,
            name=f"User {i}",
            email=email,
            active=True,
            created_at=now,
            updated_at=now,
        )
        adapter.create(user)

    # Act
    results = adapter.get_all()

    # Assert
    assert len(results) == 3


def test_update_user(db_session) -> None:
    """Test updating a user."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=None,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    created = adapter.create(user)
    created.update_name("Jane Doe")

    # Act
    result = adapter.update(created)

    # Assert
    assert result.name == "Jane Doe"


def test_delete_user(db_session) -> None:
    """Test deleting a user."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)
    now = datetime.now(UTC)
    email = EmailAddress("test@example.com")
    user = User(
        id=None,
        name="John Doe",
        email=email,
        active=True,
        created_at=now,
        updated_at=now,
    )
    created = adapter.create(user)

    # Act
    result = adapter.delete(created.id or 0)

    # Assert
    assert result is True
    assert adapter.get_by_id(created.id or 0) is None


def test_delete_user_not_found(db_session) -> None:
    """Test deleting non-existent user returns False."""
    # Arrange
    adapter = UserRepositoryPostgresAdapter(db_session)

    # Act
    result = adapter.delete(999)

    # Assert
    assert result is False
