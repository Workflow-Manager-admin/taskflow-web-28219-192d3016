from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.core.config import settings

from src.api.core import models

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Auto-create tables for development/demo only.
def init_db_tables():
    """Create all database tables if they do not exist (dev/demo convenience only)."""
    models.Base.metadata.create_all(bind=engine)


init_db_tables()


# PUBLIC_INTERFACE
def get_db():
    """FastAPI dependency for providing a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
