"""Database models for NLyzer platform.

This module contains SQLAlchemy ORM models that define the database schema
for the NLyzer platform. All models inherit from the Base class defined
in the core database module.
"""

from sqlalchemy import Boolean, Column, Integer, String

from nlyzer.core.database import Base


class User(Base):
    """User model for authentication and authorization.
    
    This model represents users in the NLyzer B2B platform, storing
    authentication credentials and basic user information.
    
    Attributes:
        id: Primary key, unique identifier for each user.
        email: User's email address, used for authentication (unique, indexed).
        hashed_password: Bcrypt hashed password for secure authentication.
        is_active: Boolean flag indicating if the user account is active.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)