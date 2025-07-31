"""Authentication API endpoints for NLyzer platform.

This module provides HTTP endpoints for user authentication including
user registration and login functionality. All endpoints follow FastAPI
conventions and use proper security practices.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from nlyzer.core.database import get_db
from nlyzer.core.models import Token, User, UserCreate
from nlyzer.core.security import create_access_token, verify_password
from nlyzer.db import crud

# Create router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user account.
    
    Creates a new user account with the provided email and password.
    The email must be unique across the platform.
    
    Args:
        user: UserCreate object containing registration data.
        db: Database session dependency.
        
    Returns:
        The newly created user data (without password).
        
    Raises:
        HTTPException: If email is already registered (400).
    """
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    return crud.create_user(db=db, user=user)


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """Authenticate user and return access token.
    
    Validates user credentials and returns a JWT access token for
    authenticated API access. Uses OAuth2 password flow.
    
    Args:
        form_data: OAuth2 form data containing username (email) and password.
        db: Database session dependency.
        
    Returns:
        Token object containing access token and token type.
        
    Raises:
        HTTPException: If credentials are invalid (401).
    """
    # Find user by email (OAuth2 uses 'username' field for email)
    user = crud.get_user_by_email(db, email=form_data.username)
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer")