import os
import shutil
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ensure backend root directory is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

DATABASE_URL = os.environ.get("DATABASE_URL")
BUNDLED_DB = BACKEND_DIR / "tools.db"

# Detect Vercel / serverless environment
IS_SERVERLESS = bool(
    os.environ.get("VERCEL")
    or os.environ.get("VERCEL_ENV")
    or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
)

if not DATABASE_URL:
    if IS_SERVERLESS:
        db_path = Path("/tmp/tools.db")
    else:
        db_path = BUNDLED_DB
    DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

_initialized = False


def create_tables() -> None:
    """Create all tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def ensure_db_initialized() -> None:
    """Initialize database with tables and seed data if needed.

    Works robustly on both local development and Vercel serverless functions
    where the root filesystem is read-only and /tmp is used.
    """
    global _initialized
    if _initialized:
        return

    # If running in serverless, copy bundled database to /tmp if available
    if IS_SERVERLESS:
        tmp_db = Path("/tmp/tools.db")
        if not tmp_db.exists() and BUNDLED_DB.exists():
            try:
                shutil.copy2(BUNDLED_DB, tmp_db)
            except Exception as e:
                print(f"[DB] Could not copy bundled DB to /tmp: {e}")

    # Ensure all tables exist
    create_tables()

    # Seed demo data if database is empty
    session = SessionLocal()
    try:
        from sqlalchemy import select as sa_select
        from app.models import Tool

        count = session.execute(sa_select(Tool)).scalars().all()
        if len(count) == 0:
            try:
                from seed import seed
                seed()
            except Exception as e:
                print(f"[DB] Failed to seed database: {e}")
    except Exception as e:
        print(f"[DB] Error verifying database content: {e}")
    finally:
        session.close()

    _initialized = True


def get_db():
    if not _initialized:
        ensure_db_initialized()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
