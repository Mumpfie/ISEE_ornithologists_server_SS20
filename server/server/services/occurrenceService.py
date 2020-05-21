import os
from typing import List
from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .. import models, schemas
from ..utils import uploadPicture

occurrence_picture_dir = './pictures/occurrence'

def clean_occurence(occurence: schemas.Occurrence) -> schemas.Occurrence:
    if (hasattr(occurence.user, "bird_occurrences") and occurence.user.bird_occurrences is not None):
        occurence.user.bird_occurrences.clear()
    if (hasattr(occurence.bird, "occurrences") and occurence.bird.occurrences is not None):
        occurence.bird.occurrences.clear()
    return occurence

def clean_occurences(occurences: List[schemas.Occurrence]) -> List[schemas.Occurrence]:
    for oc in occurences:
        clean_occurence(oc)
    return occurences

def create_occurrence(db: Session, occurrence: schemas.Occurrence):
    if occurrence.timestamp is None:
        occurrence.timestamp = datetime.now()

    user = db.query(models.User).get(occurrence.user_id)
    if user is None:
        raise HTTPException(400, "User with id {} doesn't exist".format(occurrence.user_id))
    else:
        occurrence.user = user

    bird = db.query(models.Bird).get(occurrence.bird_id)
    if bird is None:
        raise HTTPException(400, "Bird with id {} doesn't exist".format(occurrence.bird_id))
    else:
        occurrence.bird = bird

    db_occurrence = models.Occurrence(**occurrence.dict())
    print(db_occurrence)
    db.add(db_occurrence)
    db.commit()
    db.refresh(db_occurrence)

    return clean_occurence(db_occurrence)


async def add_picture_to_occurrence(db: Session, id: int, picture: UploadFile) -> schemas.Occurrence:
    occurrence = db.query(models.Occurrence).get(id)

    if occurrence is None:
        raise HTTPException(400, "Occurrence with id {} doesn't exist".format(id))

    path = Path(occurrence_picture_dir, str(occurrence.id) + '.jpeg')
    path = await uploadPicture(picture, path, override=True)

    occurrence.picture_url = str(path)
    db.commit()
    db.refresh(occurrence)

    return clean_occurence(occurrence)


def get_occurrence(db: Session, id: int):
    occurrence = db.query(models.Occurrence).get(id)
    if occurrence is None:
        return HTTPException(404, "Occurrence not found")

    return clean_occurence(occurrence)


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

    return clean_occurences(query.limit(limit).all())


def update_occurrence(db: Session, id: int, updated_occurrence: schemas.Occurrence) -> models.Occurrence:
    occurrence = db.query(models.Occurrence).get(id)

    if updated_occurrence.user_id is not None:
        if db.query(models.User).get(updated_occurrence.user_id) is None:
            raise HTTPException(400, "User with id {} doesn't exist".format(updated_occurrence.user_id))

    if updated_occurrence.bird_id is not None:
        if db.query(models.Bird).get(updated_occurrence.bird_id) is None:
            raise HTTPException(400, "Bird with id {} doesn't exist".format(updated_occurrence.bird_id))

    new_prop = updated_occurrence.dict(exclude_unset=True)
    for key, value in new_prop.items():
        setattr(occurrence, key, value)

    db.commit()
    db.refresh(occurrence)
    return clean_occurence(occurrence)


def delete_occurrence(db: Session, id: int):
    occurrence: models.Occurrence = db.query(models.Occurrence).get(id)

    if occurrence.picture_url is not None:
        pic_path: Path = Path(occurrence.picture_url)
        if pic_path.exists():
            os.remove(pic_path)

    db.delete(occurrence)
    db.commit()
    return clean_occurence(occurrence)

