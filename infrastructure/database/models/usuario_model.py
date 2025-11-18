"""Usuario database model."""

from datetime import UTC, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(UTC)


class UsuarioModel(Base):
    """Usuario ORM model."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=utc_now, nullable=False)
    fecha_actualizacion = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

