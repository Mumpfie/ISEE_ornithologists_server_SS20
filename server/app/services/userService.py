import os
from typing import List
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from model import models, schemas
from util.utils import uploadPicture

from config.config import picture_dir

user_picture_dir = picture_dir + '/user'

def create_user(db: Session, user: schemas.User) -> schemas.User:
    if get_users(db, user.name):
        raise HTTPException(422, "User already registered")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def add_picture_to_user(db: Session, id: int, picture: UploadFile) -> schemas.User:
    user = db.query(models.User).get(id)

    path = Path(user_picture_dir, str(user.id) + '.jpeg')
    path = await uploadPicture(picture, path, override=True)

    user.picture_url = str(path)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, id: int) -> schemas.User:
    return db.query(models.User).get(id)

def get_users(db: Session, name: str, skip: int = 0, limit: int = 20) -> List[schemas.User]:
    if name is None:
        return db.query(models.User).slice(skip, skip + limit).all()
    else:
        return db.query(models.User).filter(models.User.name == name).all()

def update_user(db: Session, id: int, new_prop: schemas.User) -> schemas.User:
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(422, "User not existing")

    user.name = new_prop.name

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int) -> schemas.User:
    user: models.User = db.query(models.User).get(id)

    if user.picture_url is not None:
        pic_path: Path = Path(user.picture_url)
        if pic_path.exists():
            os.remove(pic_path)

    db.query(models.Occurrence).filter(models.Occurrence.user_id == id).delete()
    db.delete(user)
    db.commit()
    return user
