## Blog Platform REST API

A fully functional **RESTful API** for a multi-user blog platform, built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Pydantic**.  
Implements CRUD operations, relationships, filtering, and proper API structure for educational and production-style use.

---

## Requirements

- Python 3.9+
- FastAPI, Uvicorn, SQLAlchemy, Pydantic

Install all dependencies:

```bash
pip  install fastapi uvicorn sqlalchemy pydantic pydantic-settings email-validator
```
Running the Project
Open a terminal in the project root (where app/ is located).

Run the FastAPI development server:

```bash
Copy code
uvicorn app.main:app --reload
You should see:

pgsql
Copy code
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
🌐 Accessing the API
Resource	URL
Swagger Docs (interactive)	http://127.0.0.1:8000/docs
ReDoc Documentation	http://127.0.0.1:8000/redoc
Health Check	http://127.0.0.1:8000/ → { "status": "ok" }
```

## 🧩 API Overview
```
Users
Method	Endpoint	Description
POST	/users	Create a new user
GET	/users	List all users (filter by partial username: ?q=)
GET	/users/{user_id}	Retrieve a specific user
PUT	/users/{user_id}	Update a user
DELETE	/users/{user_id}	Delete a user
GET	/users/{user_id}/posts	List all posts from that user

Posts
Method	Endpoint	Description
POST	/posts	Create a post (requires author_id, optional tag_ids)
GET	/posts	List posts (filter by tag: ?tag=)
GET	/posts/{post_id}	Retrieve a post
PUT	/posts/{post_id}	Update a post
DELETE	/posts/{post_id}	Delete a post
GET	/posts/{post_id}/comments	List comments for a post
POST	/posts/{post_id}/tags/{tag_id}	Link an existing tag to a post

Comments
Method	Endpoint	Description
POST	/comments	Create a comment (requires author_id)
POST	/comments/post/{post_id}	Create a comment under a specific post
GET	/comments	List all comments
GET	/comments/{comment_id}	Retrieve a comment
PUT	/comments/{comment_id}	Update a comment
DELETE	/comments/{comment_id}	Delete a comment

Tags
Method	Endpoint	Description
POST	/tags	Create a tag
GET	/tags	List all tags
GET	/tags/{tag_id}	Retrieve a tag
PUT	/tags/{tag_id}	Update a tag
DELETE	/tags/{tag_id}	Delete a tag
```
## Database
Uses SQLite, automatically created as blog.db in the project directory.

No manual setup required.

All tables are created automatically on startup.

## Example Workflow

```
Create a User

json
Copy code
POST /users
{
  "username": "alice",
  "email": "alice@example.com"
}
Create a Tag

json
Copy code
POST /tags
{ "name": "python" }
Create a Post

json
Copy code
POST /posts
{
  "title": "My first post",
  "content": "Hello, world!",
  "author_id": 1,
  "tag_ids": [1]
}
Add a Comment

json
Copy code
POST /comments/post/1
{
  "content": "Nice post!",
  "author_id": 1
}
Filter Posts by Tag
```

```bash
Copy code
GET /posts?tag=python
🧱 Project Structure
graphql
Copy code
app/
│
├── main.py          # FastAPI app entry point
├── database.py      # Database engine & session setup (SQLAlchemy + SQLite)
├── models.py        # ORM models (User, Post, Comment, Tag)
├── schemas.py       # Pydantic models for API validation
├── deps.py          # Dependency Injection setup for DB session
│
└── routers/         # API route definitions
    ├── users.py
    ├── posts.py
    ├── comments.py
    └── tags.py
    
```
## Technical Highlights
FastAPI with automatic Swagger documentation

SQLAlchemy ORM with relational models

Pydantic for request validation and data serialization

Dependency Injection (Depends(get_db))

Clear separation of concerns: models, schemas, routers, services

Consistent error handling (400, 404, 409, 422, etc.)

## Author
Lyubomir Dimov

Web Server Programming — Blog Platform API (University Project)

2025 — FastAPI · Python · SQLite