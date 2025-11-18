"""Tests for usuario router."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.models.usuario_model import Base
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


def test_create_usuario(client) -> None:
    """Test creating a usuario via API."""
    response = client.post(
        "/usuarios",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Juan Pérez"
    assert data["email"] == "juan@example.com"
    assert data["activo"] is True
    assert "id" in data


def test_create_usuario_duplicate_email(client) -> None:
    """Test creating usuario with duplicate email returns error."""
    # Create first usuario
    client.post(
        "/usuarios",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
        },
    )

    # Try to create second with same email
    response = client.post(
        "/usuarios",
        json={
            "nombre": "Pedro García",
            "email": "juan@example.com",
            "activo": True,
        },
    )
    assert response.status_code == 400


def test_get_usuario(client) -> None:
    """Test getting a usuario via API."""
    # Create usuario
    create_response = client.post(
        "/usuarios",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
        },
    )
    usuario_id = create_response.json()["id"]

    # Get usuario
    response = client.get(f"/usuarios/{usuario_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario_id
    assert data["nombre"] == "Juan Pérez"


def test_get_usuario_not_found(client) -> None:
    """Test getting non-existent usuario returns 404."""
    response = client.get("/usuarios/999")
    assert response.status_code == 404


def test_list_usuarios(client) -> None:
    """Test listing usuarios via API."""
    # Create multiple usuarios
    for i in range(3):
        client.post(
            "/usuarios",
            json={
                "nombre": f"Usuario {i}",
                "email": f"usuario{i}@example.com",
                "activo": True,
            },
        )

    # List usuarios
    response = client.get("/usuarios")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_usuario(client) -> None:
    """Test updating a usuario via API."""
    # Create usuario
    create_response = client.post(
        "/usuarios",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
        },
    )
    usuario_id = create_response.json()["id"]

    # Update usuario
    response = client.put(
        f"/usuarios/{usuario_id}",
        json={
            "nombre": "Juan Pérez Actualizado",
            "activo": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Juan Pérez Actualizado"
    assert data["activo"] is False


def test_delete_usuario(client) -> None:
    """Test deleting a usuario via API."""
    # Create usuario
    create_response = client.post(
        "/usuarios",
        json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "activo": True,
        },
    )
    usuario_id = create_response.json()["id"]

    # Delete usuario
    response = client.delete(f"/usuarios/{usuario_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/usuarios/{usuario_id}")
    assert get_response.status_code == 404
