from typing import List

from sqlalchemy.orm import Session
from ..queryClasses import Color, Shape, Size, Breeding
from fastapi import HTTPException
from .. import models, schemas

def clean_bird(bird : schemas.Bird) -> schemas.Bird:
    if(hasattr(bird, "occurrences") and bird.occurrences is not None):
        for oc in bird.occurrences:
            if(hasattr(oc.user, "bird_occurrences") and oc.user.bird_occurrences is not None):
                oc.user.bird_occurrences.clear()
            if (hasattr(oc.bird, "occurrences") and oc.bird.occurrences is not None):
                oc.bird.occurrences.clear()
    return bird

def clean_birds(birds : List[schemas.Bird]) -> List[schemas.Bird]:
    for bird in birds:
        clean_bird(bird)
    return birds

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

    return clean_birds(query.slice(skip, limit).all())


def get_bird(db: Session, id: int) -> schemas.Bird:
    bird = db.query(models.Bird).get(id)
    if bird is None:
        raise HTTPException(404, "Bird not found")
    return clean_bird(db.query(models.Bird).get(id))
