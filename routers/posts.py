from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=schemas.PostOut, status_code=201)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    author = db.get(models.User, payload.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Invalid author_id")

    post = models.Post(
        title=payload.title,
        content=payload.content,
        author_id=payload.author_id,
    )

    if payload.tag_ids:
        tags = db.scalars(
            select(models.Tag).where(models.Tag.id.in_(payload.tag_ids))
        ).all()
        if len(tags) != len(set(payload.tag_ids)):
            raise HTTPException(status_code=400, detail="Some tag_ids do not exist")
        post.tags = tags

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("", response_model=List[schemas.PostOut])
def list_posts(
    tag: Optional[str] = Query(default=None, description="Filter by tag name"),
    db: Session = Depends(get_db),
):
    stmt = select(models.Post)
    if tag:
        stmt = stmt.join(models.Post.tags).where(models.Tag.name == tag)
    return db.scalars(stmt).unique().all()


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db)
):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = payload.dict(exclude_unset=True)
    tag_ids = data.pop("tag_ids", None)

    for key, value in data.items():
        setattr(post, key, value)

    if tag_ids is not None:
        tags = db.scalars(
            select(models.Tag).where(models.Tag.id.in_(tag_ids))
        ).all()
        if len(tags) != len(set(tag_ids)):
            raise HTTPException(status_code=400, detail="Some tag_ids do not exist")
        post.tags = tags

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return


# All comments for a specific post
@router.get("/{post_id}/comments", response_model=List[schemas.CommentOut])
def get_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post.comments


# Associate existing tag with a post
@router.post("/{post_id}/tags/{tag_id}", response_model=schemas.PostOut)
def attach_tag_to_post(post_id: int, tag_id: int, db: Session = Depends(get_db)):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    tag = db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag not in post.tags:
        post.tags.append(tag)
        db.commit()
        db.refresh(post)

    return post
