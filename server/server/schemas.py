from __future__ import annotations
from typing import List
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from .queryClasses import Color, Size, Shape, Breeding


# User


class User(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str = Field(default=None, readOnly=True)
    name: str
    bird_occurrences: List[Occurrence] = Field(default=[], readOnly=True)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }

# Occurrence

class Occurrence(BaseModel):
    id: int = Field(default=None, readOnly=True)
    timestamp: datetime = None
    note: str = None
    picture_url: str = None
    longitude: float = Field(format="double")
    latitude: float = Field(format="double")
    altitude: float = Field(default=0, format="double")
    user: User = Field(readOnly=True)
    bird: Bird = Field(readOnly=True)
    user_id: int
    bird_id: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


# Bird

class Bird(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str
    taxon: str
    genus: str
    order: str
    authority: str
    color: Color
    size: Size
    shape: Shape
    breeding: Breeding
    subregion: str
    family: Family
    species: Species
    occurrences: List[Occurrence] = Field(readOnly=True, default=[])

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


# Family

class Family(BaseModel):
    name_scientific: str
    name_english: str
    name_german: str

    class Config:
        orm_mode = True


# Species

class Species(BaseModel):
    name_scientific: str
    name_english: str
    name_german: str

    class Config:
        orm_mode = True

class FileResponse(BaseModel):
    file_url: str

    class Config:
        orm_mode = True

User.update_forward_refs()
Occurrence.update_forward_refs()
Bird.update_forward_refs()
