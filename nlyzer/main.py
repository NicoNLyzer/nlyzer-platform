"""Main FastAPI application for NLyzer platform.

This is the entry point for the NLyzer B2B SaaS platform. It sets up
the FastAPI application, creates database tables, and includes all
API routers.
"""

from fastapi import FastAPI

from nlyzer.api.auth_endpoints import router as auth_router
from nlyzer.core.database import Base, engine

# Create FastAPI application
app = FastAPI(
    title="NLyzer Platform",
    description="Multimodal Conversational Commerce Platform for B2B SaaS",
    version="1.0.0"
)


@app.on_event("startup")
def create_tables():
    """Create database tables on application startup."""
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint for API health check.
    
    Returns:
        Simple health check message.
    """
    return {"message": "NLyzer Platform API is running"}