"""SQLAlchemy database models for NLyzer API."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base class for all our models
Base = declarative_base()

# TODO: Add actual model definitions here during implementation
# Example:
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     ...