import os
from typing import List
from pathlib import Path
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .userService import get_users, get_user
from .. import models, schemas
from ..utils import uploadPicture

occurrence_picture_dir = './pictures/occurrence'

def create_occurrence(db: Session, occurrence: schemas.Occurrence):
    if occurrence.timestamp is None:
        occurrence.timestamp = datetime.utcnow()
    else:
        occurrence.timestamp = occurrence.timestamp.astimezone(timezone.utc)

    user : schemas.User = db.query(models.User).get(occurrence.user_id)
    if user is None:
        raise HTTPException(400, "User with id {} doesn't exist".format(occurrence.user_id))
    else:
        occurrence.user = user

    bird : schemas.Bird = db.query(models.Bird).get(occurrence.bird_id)
    if bird is None:
        raise HTTPException(400, "Bird with id {} doesn't exist".format(occurrence.bird_id))
    else:
        occurrence.bird = bird

    db_occurrence = models.Occurrence(**occurrence.dict())
    print(db_occurrence)
    db.add(db_occurrence)
    db.commit()
    db.refresh(db_occurrence)
    return db_occurrence


async def add_picture_to_occurrence(db: Session, id: int, picture: UploadFile) -> schemas.Occurrence:
    occurrence = db.query(models.Occurrence).get(id)

    if occurrence is None:
        raise HTTPException(422, "Occurrence with id {} doesn't exist".format(id))

    path = Path(occurrence_picture_dir, str(occurrence.id) + '.jpeg')
    path = await uploadPicture(picture, path, override=True)

    occurrence.picture_url = str(path)
    db.commit()
    db.refresh(occurrence)
    return occurrence


def get_occurrence(db: Session, id: int):
    occurrence = db.query(models.Occurrence).get(id)
    if occurrence is None:
        raise HTTPException(404, "Occurrence not found")

    return occurrence


def get_occurrences(
        db: Session,
        user_id: int = None,
        bird_id: int = None,
        from_ts: datetime = None,
        to_ts: datetime = None,
        latitude: float = None,
        longitude: float = None,
        radius: float = None,
        limit: int = 20
) -> List[schemas.Occurrence]:
    query = db.query(models.Occurrence)

    if (latitude is None or longitude is None or radius is None ) and\
            (latitude is not None or longitude is not None or radius is not None):
        raise HTTPException(400, "All of latitude, longitude and radius have to be defined or none of them")


    if user_id:
        query = query.filter(models.Occurrence.user_id == user_id)
    if bird_id:
        query = query.filter(models.Occurrence.bird_id == bird_id)
    if from_ts:
        query = query.filter(models.Occurrence.timestamp >= from_ts)
    if to_ts:
        query = query.filter(models.Occurrence.timestamp <= to_ts)
    if latitude is not None and longitude is not None and radius is not None:
        query = query.filter((models.Occurrence.latitude - latitude) * (models.Occurrence.latitude - latitude) +
                             (models.Occurrence.longitude - longitude) * (models.Occurrence.longitude - longitude) <=
                             radius * radius)

    return query.limit(limit).all()


def update_occurrence(db: Session, id: int, updated_occurrence: schemas.Occurrence) -> models.Occurrence:
    occurrence: models.Occurrence = db.query(models.Occurrence).get(id)

    if updated_occurrence.user_id is not None:
        new_user: models.User = db.query(models.User).get(updated_occurrence.user_id)
        if new_user is None:
            raise HTTPException(400, "User with id {} doesn't exist".format(updated_occurrence.user_id))
        else:
            updated_occurrence.user = new_user

    if updated_occurrence.bird_id is not None:
        new_bird: models.Bird = db.query(models.Bird).get(updated_occurrence.bird_id)
        if new_bird is None:
            raise HTTPException(400, "Bird with id {} doesn't exist".format(updated_occurrence.bird_id))
        else:
            updated_occurrence.bird = new_bird

    new_prop = updated_occurrence.dict()
    for key, value in new_prop.items():
        setattr(occurrence, key, value)

    db.commit()
    db.refresh(occurrence)
    return occurrence


def delete_occurrence(db: Session, id: int):
    occurrence: models.Occurrence = db.query(models.Occurrence).get(id)

    if occurrence.picture_url is not None:
        pic_path: Path = Path(occurrence.picture_url)
        if pic_path.exists():
            os.remove(pic_path)

    db.delete(occurrence)
    db.commit()
    return occurrence

