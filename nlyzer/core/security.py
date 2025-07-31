"""Security utilities for NLyzer authentication system.

This module provides core security functions for password hashing and JWT token
management. It uses bcrypt for secure password hashing and python-jose for
JWT token generation and validation.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from .config import settings

# Create password hashing context with bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash.
    
    Uses the configured password context to safely verify if a plain text
    password matches its hashed version.
    
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The bcrypt hashed password to compare against.
        
    Returns:
        True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the given password.
    
    Creates a secure bcrypt hash of the provided password that can be
    safely stored in the database.
    
    Args:
        password: The plain text password to hash.
        
    Returns:
        The bcrypt hashed version of the password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with the provided data.
    
    Generates a JWT token containing the provided data payload with an
    expiration time. If no expiration delta is provided, defaults to
    the configured ACCESS_TOKEN_EXPIRE_MINUTES setting.
    
    Args:
        data: Dictionary containing the claims to encode in the JWT token.
        expires_delta: Optional timedelta for token expiration. If None,
                      defaults to configured ACCESS_TOKEN_EXPIRE_MINUTES.
                      
    Returns:
        The encoded JWT token as a string.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use configured expiration time
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt