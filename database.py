from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local SQLite database (the file will be created automatically)
DATABASE_URL = "sqlite:///./blog.db"

# Create the database engine (the core connection to the DB)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite when using FastAPI
)

# Create a session factory for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all ORM models will inherit from (User, Post, etc.)
Base = declarative_base()
