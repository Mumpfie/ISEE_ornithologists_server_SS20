from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from model import models, schemas


def get_families(db: Session, name_scientific: str) -> List[schemas.Family]:
    family = db.query(models.Family).get(name_scientific)
    if family is None:
        raise HTTPException(404, "Family not found")
    return family
