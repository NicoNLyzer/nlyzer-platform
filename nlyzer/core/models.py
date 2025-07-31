"""Core Pydantic models for NLyzer authentication system.

This module contains the fundamental data models used for user authentication
and authorization throughout the NLyzer B2B platform.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model with common fields.
    
    This model serves as the foundation for other user-related models,
    containing the essential fields shared across different use cases.
    
    Attributes:
        email: User's email address (validated as proper email format).
        is_active: Flag indicating if the user account is active.
    """
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    """Model for user registration/creation.
    
    Extends UserBase with password field required during user creation.
    This model is used when processing user registration requests.
    
    Attributes:
        password: User's plaintext password (will be hashed before storage).
    """
    password: str


class User(UserBase):
    """Database representation of a user.
    
    Extends UserBase with database-specific fields. This model represents
    how user data is stored and retrieved from the database.
    
    Attributes:
        id: Unique identifier for the user in the database.
    """
    id: int
    
    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True


class Token(BaseModel):
    """JWT token response model.
    
    Used to structure the authentication token response sent to clients
    after successful login.
    
    Attributes:
        access_token: The JWT access token string.
        token_type: Type of token (typically "bearer").
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data model.
    
    Represents the data encoded within the JWT token payload.
    Used for token validation and user identification.
    
    Attributes:
        email: User's email address extracted from token (optional).
    """
    email: str | None = None