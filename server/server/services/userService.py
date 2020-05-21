from typing import List
from pathlib import Path

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .. import models, schemas
from ..utils import uploadPicture

user_picture_dir = './pictures/user'

def clean_user(user: schemas.User) -> schemas.User:
    for oc in user.bird_occurrences:
        if (hasattr(oc.user, "bird_occurrences") and oc.user.bird_occurrences is not None):
            oc.user.bird_occurrences.clear()
        if (hasattr(oc.bird, "occurrences") and oc.bird.occurrences is not None):
            oc.bird.occurrences.clear()
    return user

def clean_user_list(users : List[schemas.User]) -> List[schemas.User]:
    for user in users:
        clean_user(user)
    return users

def create_user(db: Session, user: schemas.User) -> schemas.User:
    if get_users(db, user.name):
        raise HTTPException(422, "User already registered")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return clean_user(db_user)


async def add_picture_to_user(db: Session, id: int, picture: UploadFile) -> schemas.User:
    user = db.query(models.User).get(id)

    path = Path(user_picture_dir, str(user.id) + '.jpeg')
    path = await uploadPicture(picture, path, override=True)

    user.picture_url = str(path)
    db.commit()
    db.refresh(user)
    return clean_user(user)


def get_user(db: Session, id: int) -> schemas.User:
    return clean_user(db.query(models.User).get(id))

def get_users(db: Session, name: str, skip: int = 0, limit: int = 20) -> List[schemas.User]:
    if name is None:
        return clean_user_list(db.query(models.User).slice(skip, limit).all())
    else:
        return clean_user_list(db.query(models.User).filter(models.User.name == name).all())

def update_user(db: Session, id: int, new_prop: schemas.User) -> schemas.User:
    user = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(422, "User not existing")

    user.name = new_prop.name

    db.commit()
    db.refresh(user)
    return clean_user(user)


def delete_user(db: Session, id: int) -> schemas.User:
    user = db.query(models.User).get(id)
    db.delete(user)
    db.commit()
    return clean_user(user)
