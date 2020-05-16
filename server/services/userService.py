from typing import List
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .. import models, schemas
from ..utils import uploadPicture

user_picture_dir = './pictures/user'


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
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


def read_user(db: Session, id: int) -> schemas.User:
    return db.query(models.User).get(id)


def query_user(db: Session, name: str = None) -> List[schemas.User]:
    if name:
        print('test')
        return db.query(models.User).filter(models.User.name == name).all()
    else:
        print('test123')
        return db.query(models.User).all()


def update_user(db: Session, id: int, new_prop: schemas.UserCreate) -> schemas.User:
    user = db.query(models.User).get(id)

    for attr, value in new_prop.dict().items():
        setattr(user, attr, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int) -> schemas.User:
    user = db.query(models.User).get(id)
    db.delete(user)
    db.commit()
    return user
