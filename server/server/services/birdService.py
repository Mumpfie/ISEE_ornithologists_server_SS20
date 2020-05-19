from typing import List

from sqlalchemy.orm import Session
from ..queryClasses import Color, Shape, Size, Breeding
from fastapi import HTTPException
from .. import models, schemas


def get_birds(
        db: Session,
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        skip: int = 0,
        limit: int = 20
) -> List[schemas.Bird]:
    query = db.query(models.Bird)

    if color is not None:
        query.filter(models.Color.color == color)
    if size is not None:
        query.filter(models.Size.size == size)
    if shape is not None:
        query.filter(models.Shape.shape == shape)
    if breeding is not None:
        query.filter(models.Bird.breeding == breeding)

    return query.slice(skip, limit).all()


def get_bird(db: Session, id: int) -> schemas.Bird:
    bird = db.query(models.Bird).get(id)
    if bird is None:
        raise HTTPException(404, "Bird not found")
    return db.query(models.Bird).get(id)
