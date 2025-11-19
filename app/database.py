import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings


# Only use check_same_thread for SQLite
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    print(f"Creating database engine with URL: {settings.database_url[:20]}...", file=sys.stderr)
    engine = create_engine(
        settings.database_url, 
        connect_args=connect_args,
        pool_pre_ping=True  # Verify connections before using
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✓ Database engine created", file=sys.stderr)
except Exception as e:
    print(f"❌ Error creating database engine: {e}", file=sys.stderr)
    raise

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

