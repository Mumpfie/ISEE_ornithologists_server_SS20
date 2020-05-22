from __future__ import annotations
from typing import List
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from .queryClasses import Color, Size, Shape, Breeding


# User

class UserBase(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str = Field(default=None, readOnly=True)
    name: str

    class Config:
        orm_mode = True

class User(UserBase):
    bird_occurrences: List[Occurrence] = Field(default=[], readOnly=True, nullable=False)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }

# Occurrence

class Occurrence(BaseModel):
    id: int = Field(default=None, readOnly=True)
    timestamp: datetime = None
    note: str = None
    picture_url: str = Field(default=None, readOnly=True)
    longitude: float = Field(format="double")
    latitude: float = Field(format="double")
    altitude: float = Field(default=0, format="double")
    user: UserBase = Field(default=None, readOnly=True)
    bird: BirdBase = Field(default=None, readOnly=True)
    user_id: int
    bird_id: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }


# Bird

class BirdBase(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str = None
    taxon: str
    genus: str
    order: str
    authority: str = None
    color: Color = None
    size: Size = None
    shape: Shape = None
    breeding: Breeding = None
    subregion: str = None
    family: Family
    species: Species

    class Config:
        orm_mode = True

class Bird(BirdBase):
    occurrences: List[Occurrence] = Field(default=[], readOnly=True, nullable=False)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }


# Family

class Family(BaseModel):
    name_scientific: str
    name_english: str = None
    name_german: str = None

    class Config:
        orm_mode = True


# Species

class Species(BaseModel):
    name_scientific: str
    name_english: str = None
    name_german: str = None

    class Config:
        orm_mode = True


class FileResponse(BaseModel):
    file_url: str

    class Config:
        orm_mode = True


User.update_forward_refs()
UserBase.update_forward_refs()
Occurrence.update_forward_refs()
Bird.update_forward_refs()
BirdBase.update_forward_refs()
