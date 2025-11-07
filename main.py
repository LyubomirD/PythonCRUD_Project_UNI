from fastapi import FastAPI
from .database import Base, engine
from .routers import users, posts, comments, tags

# Create all tables in the database (if they do not exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Platform API", version="1.0")

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(tags.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
