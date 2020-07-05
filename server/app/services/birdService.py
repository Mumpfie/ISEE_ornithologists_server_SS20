import os
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from config.config import picture_dir
from .occurrenceService import get_occurrences
from model.queryClasses import Color, Shape, Size, Breeding
from fastapi import HTTPException
from fastapi.responses import FileResponse
from model import models, schemas

bird_picture_dir = picture_dir + "/bird"

def get_birds(
        db: Session,
        part_name: str = None,
        language: str = 'en',
        color: Color = None,
        size: Size = None,
        shape: Shape = None,
        breeding: Breeding = None,
        skip: int = 0,
        limit: int = 20
) -> List[schemas.Bird]:
    query = db.query(models.Bird)

    if part_name is not None and language=='en':
        query = query.filter(func.lower(models.Bird.species_name_english).contains(func.lower(part_name)))
    if part_name is not None and language=='de':
        query = query.filter(func.lower(models.Bird.species_name_german).contains(func.lower(part_name)))
    if color is not None:
        query = query.filter(models.Bird.color == color)
    if size is not None:
        query = query.filter(models.Bird.size == size)
    if shape is not None:
        query = query.filter(models.Bird.shape == shape)
    if breeding is not None:
        query = query.filter(models.Bird.breeding == breeding)
    birds = query.slice(skip, limit).all()
    for bird in birds:
        bird.occurrences = get_occurrences(db, bird_id=bird.id)
    return birds


def get_bird(db: Session, id: int) -> schemas.Bird:
    bird = db.query(models.Bird).get(id)
    if bird is None:
        raise HTTPException(404, "Bird not found")
    bird = db.query(models.Bird).get(id)
    bird.occurrences = get_occurrences(db, bird_id=bird.id)
    return bird

async def get_bird_picture(db: Session, id: int) -> FileResponse:
    picture = get_bird(db, id).picture_url
    if (not os.path.isfile(bird_picture_dir + picture)):
        raise HTTPException(404, "Picture does not exist")
    return FileResponse(bird_picture_dir + picture, 200)