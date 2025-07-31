"""Database connection and session management for NLyzer platform.

This module provides SQLAlchemy database setup, session management, and
base model class for the NLyzer platform. It uses PostgreSQL as the
primary database with connection details loaded from configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
# For PostgreSQL, we don't need check_same_thread=False like we would for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class for database sessions
# Each SessionLocal instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for database models
# All database models will inherit from this base class
Base = declarative_base()


def get_db():
    """Create and yield a database session.
    
    This function creates a new database session and yields it for use
    in dependency injection. The session is automatically closed after use.
    
    Yields:
        Session: SQLAlchemy database session for performing database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()