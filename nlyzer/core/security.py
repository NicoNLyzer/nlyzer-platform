"""Security utilities for NLyzer authentication system.

This module provides core security functions for password hashing and JWT token
management. It uses bcrypt for secure password hashing and python-jose for
JWT token generation and validation.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

# Temporary constants - will be moved to config.py later
SECRET_KEY = "a_very_secret_key_that_will_be_replaced"
ALGORITHM = "HS256"

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
    15 minutes from creation time.
    
    Args:
        data: Dictionary containing the claims to encode in the JWT token.
        expires_delta: Optional timedelta for token expiration. If None,
                      defaults to 15 minutes.
                      
    Returns:
        The encoded JWT token as a string.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration of 15 minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt