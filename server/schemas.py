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


class User(UserBase):
    bird_occurrences: List[Occurrence] = []

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


User.update_forward_refs()


class UserCreate(UserBase):
    pass


# Occurrence

class OccurrenceBase(BaseModel):
    id: int = Field(default=None, readOnly=True)
    timestamp: datetime = None
    note: str = None
    picture_url: str = None
    longitude: float = Field(format="double")
    latitude: float = Field(format="double")
    altitude: float = Field(default=0, format="double")


class Occurrence(OccurrenceBase):
    user: User
    bird: BirdBase

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


Occurrence.update_forward_refs()


class OccurrenceCreate(OccurrenceBase):
    user_id: int
    bird_id: int


# Bird

class BirdBase(BaseModel):
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

    class Config:
        orm_mode = True

BirdBase.update_forward_refs()


class Bird(BirdBase):
    occurrences: List[Occurrence] = []

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
