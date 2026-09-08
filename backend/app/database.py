from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALITE_URL = "sqlite:///./tools.db"

engine = create_engine(
    SQLALITE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all tables if they do not exist.

    This is suitable for local development and demos. For production,
    use proper database migrations.
    """
    Base.metadata.create_all(bind=engine)
