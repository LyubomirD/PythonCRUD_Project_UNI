from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


# Create comment for a specific post (special endpoint)
@router.post("/post/{post_id}", response_model=schemas.CommentOut, status_code=201)
def create_comment_for_post(
    post_id: int, payload: schemas.CommentCreate, db: Session = Depends(get_db)
):
    post = db.get(models.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    author = db.get(models.User, payload.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Invalid author_id")

    comment = models.Comment(
        content=payload.content,
        author_id=payload.author_id,
        post_id=post_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# Generic CRUD (optional but nice to have)

@router.post("", response_model=schemas.CommentOut, status_code=201)
def create_comment(payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    if not db.get(models.User, payload.author_id):
        raise HTTPException(status_code=400, detail="Invalid author_id")
    comment = models.Comment(**payload.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("", response_model=List[schemas.CommentOut])
def list_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()


@router.get("/{comment_id}", response_model=schemas.CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=schemas.CommentOut)
def update_comment(
    comment_id: int, payload: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(comment, key, value)

    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(models.Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return
