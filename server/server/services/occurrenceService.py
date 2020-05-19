from typing import List
from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from .. import models, schemas
from ..utils import uploadPicture

occurrence_picture_dir = './pictures/occurrence'


def create_occurrence(db: Session, occurrence: schemas.Occurrence):
    if occurrence.timestamp is None:
        occurrence.timestamp = datetime.now()

    db_occurrence = models.Occurrence(**occurrence.dict())
    print(db_occurrence)
    db.add(db_occurrence)
    db.commit()
    db.refresh(db_occurrence)
    return db_occurrence


async def add_picture_to_occurrence(db: Session, id: int, picture: UploadFile) -> schemas.Occurrence:
    occurrence = db.query(models.Occurrence).get(id)

    path = Path(occurrence_picture_dir, str(occurrence.id) + '.jpeg')
    path = await uploadPicture(picture, path, override=True)

    occurrence.picture_url = str(path)
    db.commit()
    db.refresh(occurrence)
    return occurrence


def get_occurrence(db: Session, id: int):
    occurrence = db.query(models.Occurrence).get(id)
    if occurrence is None:
        return HTTPException(404, "Occurrence not found")
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

    if user_id:
        query = query.filter(models.Occurrence.user_id == user_id)
    if bird_id:
        query = query.filter(models.Occurrence.bird_id == bird_id)
    if from_ts:
        query = query.filter(models.Occurrence.timestamp >= from_ts)
    if to_ts:
        query = query.filter(models.Occurrence.timestamp <= to_ts)
    if latitude and longitude and radius:
        query = query.filter((models.Occurrence.latitude - latitude) * (models.Occurrence.latitude - latitude) +
                             (models.Occurrence.longitude - longitude) * (models.Occurrence.longitude - longitude) <=
                             radius * radius)

    return query.limit(limit).all()


def update_occurrence(db: Session, id: int, updated_occurrence: schemas.Occurrence) -> models.Occurrence:
    occurrence = db.query(models.Occurrence).get(id)

    if updated_occurrence.timestamp is not None:
        occurrence.timestamp = updated_occurrence.timestamp
    if updated_occurrence.note is not None:
        occurrence.note = updated_occurrence.note
    if updated_occurrence.picture_url is not None:
        occurrence.picture_url = updated_occurrence.picture_url
    if updated_occurrence.longitude is not None:
        occurrence.longitude = updated_occurrence.longitude
    if updated_occurrence.latitude is not None:
        occurrence.latitude = updated_occurrence.latitude
    if updated_occurrence.altitude is not None:
        occurrence.altitude = updated_occurrence.altitude
    if updated_occurrence.user_id is not None:
        occurrence.user_id = updated_occurrence.user_id
    if updated_occurrence.bird_id is not None:
        occurrence.bird_id = updated_occurrence.bird_id

    db.commit()
    db.refresh(occurrence)
    return occurrence


def delete_occurrence(db: Session, id: int):
    occurrence = db.query(models.Occurrence).get(id)
    db.delete(occurrence)
    db.commit()
    return occurrence

