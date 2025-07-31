"""CRUD operations for NLyzer database models.

This module provides Create, Read, Update, Delete operations for database
models. All functions follow the repository pattern and accept a SQLAlchemy
session for database operations.
"""

from sqlalchemy.orm import Session

from nlyzer.core.models import UserCreate
from nlyzer.core.security import get_password_hash

from .models import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by their email address.
    
    Queries the database to find a user with the specified email address.
    
    Args:
        db: SQLAlchemy database session.
        email: Email address to search for.
        
    Returns:
        User object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database.
    
    Takes a Pydantic UserCreate object, hashes the password securely,
    creates a new SQLAlchemy User model instance, and saves it to the database.
    
    Args:
        db: SQLAlchemy database session.
        user: Pydantic UserCreate object containing user data.
        
    Returns:
        The newly created User object from the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user