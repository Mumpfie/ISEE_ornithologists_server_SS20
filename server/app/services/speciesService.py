from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from model import models, schemas


def get_species(db: Session, name_scientific: str) -> List[schemas.Species]:
    species = db.query(models.Species).get(name_scientific)
    if species is None:
        raise HTTPException(404, "Species not found")
    return species
