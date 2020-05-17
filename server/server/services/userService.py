from typing import List
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .. import models, schemas
from ..utils import uploadPicture

user_picture_dir = './pictures/user'


def create_user(db: Session, user: schemas.User) -> schemas.User:
    if(get_users(db, user.name)):
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

def get_users(db: Session, name: str, skip: int, limit: int) -> List[schemas.User]:
    if(name is None):
        return db.query(models.User).slice(skip, limit).all()
    else:
        return db.query(models.User).filter(models.User.name == name).all()

def update_user(db: Session, id: int, new_prop: schemas.User) -> schemas.User:
    user = db.query(models.User).get(id)
    if (user is None):
        raise HTTPException(422, "User not existing")

    user.name = new_prop.name

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int) -> schemas.User:
    user = db.query(models.User).get(id)
    db.delete(user)
    db.commit()
    return user
