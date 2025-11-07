from .database import SessionLocal

# Provides a database session to path operations via Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
