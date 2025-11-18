"""PostgreSQL adapter for User repository."""

from typing import List, Optional

from sqlalchemy.orm import Session

from core.application.ports.user_repository_port import (
    UserRepositoryPort,
)
from core.domain.entities.user import User
from core.domain.value_objects.email_address import EmailAddress
from infrastructure.database.models.user_model import UserModel


class UserRepositoryPostgresAdapter(UserRepositoryPort):
    """PostgreSQL implementation of UserRepositoryPort."""

    def __init__(self, db: Session) -> None:
        """Initialize adapter with database session."""
        self._db = db

    def create(self, user: User) -> User:
        """Create a new user."""
        db_user = UserModel(
            name=user.name,
            email=str(user.email),
            active=user.active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)

        return self._to_domain_entity(db_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id."""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        if not db_user:
            return None
        return self._to_domain_entity(db_user)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        if not db_user:
            return None
        return self._to_domain_entity(db_user)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        db_users = (
            self._db.query(UserModel).offset(skip).limit(limit).all()
        )
        return [
            self._to_domain_entity(db_user)
            for db_user in db_users
        ]

    def update(self, user: User) -> User:
        """Update an existing user."""
        if not user.id:
            raise ValueError("User id is required for update")

        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user.id)
            .first()
        )
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")

        db_user.name = user.name
        db_user.email = str(user.email)
        db_user.active = user.active
        db_user.updated_at = user.updated_at

        self._db.commit()
        self._db.refresh(db_user)

        return self._to_domain_entity(db_user)

    def delete(self, user_id: int) -> bool:
        """Delete a user by id."""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        if not db_user:
            return False

        self._db.delete(db_user)
        self._db.commit()
        return True

    @staticmethod
    def _to_domain_entity(db_user: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=db_user.id,
            name=db_user.name,
            email=EmailAddress(db_user.email),
            active=db_user.active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
