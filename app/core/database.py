# app/core/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse database name from URL
def get_db_name(url: str) -> str:
    return url.split('/')[-1]

# Main engine (will connect to the specific database)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_database():
    """Reset database - creates DB if it doesn't exist (MySQL compatible)"""
    try:
        db_name = get_db_name(settings.DATABASE_URL)
        
        # Create a temporary engine without database name
        base_url = '/'.join(settings.DATABASE_URL.split('/')[:-1])
        temp_engine = create_engine(base_url, pool_pre_ping=True)
        
        with temp_engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            conn.execute(text(f"DROP DATABASE IF EXISTS {db_name};"))
            conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            conn.commit()
        
        logger.info(f"✅ Database '{db_name}' recreated.")
        
        # Now create tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ All tables created successfully.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database reset failed: {e}")
        return False