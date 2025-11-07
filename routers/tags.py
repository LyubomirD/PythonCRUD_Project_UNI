from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=List[schemas.TagOut])
def list_tags(db: Session = Depends(get_db)):
    return db.scalars(select(models.Tag)).all()


@router.get("/{tag_id}", response_model=schemas.TagOut)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("", response_model=schemas.TagOut, status_code=201)
def create_tag(payload: schemas.TagCreate, db: Session = Depends(get_db)):
    if db.scalar(select(models.Tag).where(models.Tag.name == payload.name)):
        raise HTTPException(status_code=409, detail="Tag already exists")
    tag = models.Tag(**payload.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.put("/{tag_id}", response_model=schemas.TagOut)
def update_tag(tag_id: int, payload: schemas.TagUpdate, db: Session = Depends(get_db)):
    tag = db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(tag, key, value)

    db.commit()
    db.refresh(tag)
    return tag


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return
