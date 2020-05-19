from __future__ import annotations
from typing import List
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from .queryClasses import Color, Size, Shape, Breeding


# User

class BaseUser(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str = Field(default=None, readOnly=True)
    name: str

    class Config:
        orm_mode = True


class User(BaseUser):
    bird_occurrences: List[BaseOccurrence] = []  # Field(default=[], readOnly=True)  # TODO: infinite recursion

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


# Occurrence

class BaseOccurrence(BaseModel):
    id: int = Field(default=None, readOnly=True)
    timestamp: datetime = None
    note: str = None
    picture_url: str = Field(default=None, readOnly=True)
    longitude: float = Field(format="double")
    latitude: float = Field(format="double")
    altitude: float = Field(default=0, format="double")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
        }


class Occurrence(BaseOccurrence):
    user: BaseUser  # = Field(default=None, readOnly=True)  # TODO: value still required
    bird: BaseBird  # = Field(default=None, readOnly=True)  # TODO: value still required


class OccurrenceCreate(BaseOccurrence):
    user_id: int
    bird_id: int


class OccurrenceUpdate(OccurrenceCreate):
    timestamp: datetime = None
    note: str = None
    longitude: float = Field(default=None, format="double")
    latitude: float = Field(default=None, format="double")
    altitude: float = Field(default=None, format="double")
    user_id: int = None
    bird_id: int = None

    # Dberschreiben des Defaultwertes hat nicht funktioniert

    # class Config:
    #     fields = {
    #         'longitude': {'default': None},
    #         'latitude': {'default': None},
    #         'altitude': {'default': None},
    #         'user_id': {'default': None},
    #         'bird_id': {'default': None}
    #     }


# Bird

class BaseBird(BaseModel):
    id: int = Field(default=None, readOnly=True)
    picture_url: str = None
    taxon: str
    genus: str
    order: str
    authority: str
    color: Color
    size: Size
    shape: Shape
    breeding: Breeding
    subregion: str = None
    family: Family
    species: Species

    class Config:
        orm_mode = True


class Bird(BaseBird):
    occurrences: List[BaseOccurrence] = []  # Field(default=[], readOnly=True)  # TODO: infinite recursion

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(
                microsecond=0, tzinfo=timezone.utc
            ).isoformat()
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
Occurrence.update_forward_refs()
BaseBird.update_forward_refs()
Bird.update_forward_refs()
