"""Initialize database tables."""

from infrastructure.database.models.usuario_model import Base
from infrastructure.database.session import engine


def init_db() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
