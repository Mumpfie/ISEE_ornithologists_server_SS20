from typing import List

from sqlalchemy.orm import Session
from ..queryClasses import Color, Shape, Size, Breeding
from fastapi import HTTPException
from .. import models, schemas

def get_birds(
        db: Session,
        part_name: str = None,
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        skip: int = 0,
        limit: int = 20
) -> List[schemas.Bird]:
    query = db.query(models.Bird)

    if part_name is not None:
        query = query.filter(models.Species.name_english.contains(part_name))
    if color is not None:
        query = query.filter(models.Bird.color == color)
    if size is not None:
        query = query.filter(models.Bird.size == size)
    if shape is not None:
        query = query.filter(models.Bird.shape == shape)
    if breeding is not None:
        query = query.filter(models.Bird.breeding == breeding)

    return query.slice(skip, limit).all()


def get_bird(db: Session, id: int) -> schemas.Bird:
    bird = db.query(models.Bird).get(id)
    if bird is None:
        raise HTTPException(404, "Bird not found")
    return db.query(models.Bird).get(id)
