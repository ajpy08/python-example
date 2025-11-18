"""PostgreSQL adapter for Usuario repository."""

from typing import List, Optional

from sqlalchemy.orm import Session

from core.application.ports.usuario_repository_port import UsuarioRepositoryPort
from core.domain.entities.usuario import Usuario
from core.domain.value_objects.email_address import EmailAddress
from infrastructure.database.models.usuario_model import UsuarioModel


class UsuarioRepositoryPostgresAdapter(UsuarioRepositoryPort):
    """PostgreSQL implementation of UsuarioRepositoryPort."""

    def __init__(self, db: Session) -> None:
        """Initialize adapter with database session."""
        self._db = db

    def create(self, usuario: Usuario) -> Usuario:
        """Create a new usuario."""
        db_usuario = UsuarioModel(
            nombre=usuario.nombre,
            email=str(usuario.email),
            activo=usuario.activo,
            fecha_creacion=usuario.fecha_creacion,
            fecha_actualizacion=usuario.fecha_actualizacion,
        )
        self._db.add(db_usuario)
        self._db.commit()
        self._db.refresh(db_usuario)

        return self._to_domain_entity(db_usuario)

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Get usuario by id."""
        db_usuario = self._db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        if not db_usuario:
            return None
        return self._to_domain_entity(db_usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Get usuario by email."""
        db_usuario = (
            self._db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        )
        if not db_usuario:
            return None
        return self._to_domain_entity(db_usuario)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Get all usuarios with pagination."""
        db_usuarios = (
            self._db.query(UsuarioModel).offset(skip).limit(limit).all()
        )
        return [self._to_domain_entity(db_usuario) for db_usuario in db_usuarios]

    def update(self, usuario: Usuario) -> Usuario:
        """Update an existing usuario."""
        if not usuario.id:
            raise ValueError("Usuario id is required for update")

        db_usuario = (
            self._db.query(UsuarioModel).filter(UsuarioModel.id == usuario.id).first()
        )
        if not db_usuario:
            raise ValueError(f"Usuario with id {usuario.id} not found")

        db_usuario.nombre = usuario.nombre
        db_usuario.email = str(usuario.email)
        db_usuario.activo = usuario.activo
        db_usuario.fecha_actualizacion = usuario.fecha_actualizacion

        self._db.commit()
        self._db.refresh(db_usuario)

        return self._to_domain_entity(db_usuario)

    def delete(self, usuario_id: int) -> bool:
        """Delete a usuario by id."""
        db_usuario = (
            self._db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
        )
        if not db_usuario:
            return False

        self._db.delete(db_usuario)
        self._db.commit()
        return True

    @staticmethod
    def _to_domain_entity(db_usuario: UsuarioModel) -> Usuario:
        """Convert database model to domain entity."""
        return Usuario(
            id=db_usuario.id,
            nombre=db_usuario.nombre,
            email=EmailAddress(db_usuario.email),
            activo=db_usuario.activo,
            fecha_creacion=db_usuario.fecha_creacion,
            fecha_actualizacion=db_usuario.fecha_actualizacion,
        )

