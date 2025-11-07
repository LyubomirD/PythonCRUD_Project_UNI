from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# -------- User --------

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------- Tag --------

class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)


class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True


# -------- Post --------

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str


class PostCreate(PostBase):
    author_id: int
    tag_ids: List[int] = []


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class PostOut(PostBase):
    id: int
    created_at: datetime
    author_id: int
    tags: List[TagOut] = []

    class Config:
        from_attributes = True


# -------- Comment --------

class CommentBase(BaseModel):
    content: str = Field(min_length=1)


class CommentCreate(CommentBase):
    author_id: int


class CommentUpdate(BaseModel):
    content: Optional[str] = Field(default=None, min_length=1)


class CommentOut(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        from_attributes = True
