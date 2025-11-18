"""Tests for user router."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.models.user_model import Base
from main import app


@pytest.fixture
def client():
    """Create a test client."""
    # Override get_db dependency
    from infrastructure.database.session import get_db

    # Create test database engine
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine, autocommit=False, autoflush=False
    )

    def override_get_db():
        # Ensure tables exist before creating session
        Base.metadata.create_all(bind=engine)
        session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_create_user(client) -> None:
    """Test creating a user via API."""
    response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["active"] is True
    assert "id" in data


def test_create_user_duplicate_email(client) -> None:
    """Test creating user with duplicate email returns error."""
    # Create first user
    client.post(
        "/users",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        },
    )

    # Try to create second with same email
    response = client.post(
        "/users",
        json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "active": True,
        },
    )
    assert response.status_code == 400


def test_get_user(client) -> None:
    """Test getting a user via API."""
    # Create user
    create_response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        },
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John Doe"


def test_get_user_not_found(client) -> None:
    """Test getting non-existent user returns 404."""
    response = client.get("/users/999")
    assert response.status_code == 404


def test_list_users(client) -> None:
    """Test listing users via API."""
    # Create multiple users
    for i in range(3):
        client.post(
            "/users",
            json={
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "active": True,
            },
        )

    # List users
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_user(client) -> None:
    """Test updating a user via API."""
    # Create user
    create_response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        },
    )
    user_id = create_response.json()["id"]

    # Update user
    response = client.put(
        f"/users/{user_id}",
        json={
            "name": "John Doe Updated",
            "active": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe Updated"
    assert data["active"] is False


def test_delete_user(client) -> None:
    """Test deleting a user via API."""
    # Create user
    create_response = client.post(
        "/users",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "active": True,
        },
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
