from __future__ import annotations
from typing import List
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from .queryClasses import Color, Size, Shape, Breeding


# User

class UserBase(BaseModel):
    id: int = Field(default=None, readOnly=True)
    name: str = Field(max_length=25)

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
    longitude: float = Field(format="double", ge=-180, le=180)
    latitude: float = Field(format="double", ge=-90, le=90)
    altitude: float = Field(default=0, format="double", ge=0, le=10000)
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
    taxon: str = Field(max_length=25)
    genus: str = Field(max_length=25)
    order: str = Field(max_length=25)
    authority: str = Field(default=None, max_length=40)
    color: Color = None
    size: Size = None
    shape: Shape = None
    breeding: Breeding = None
    subregion: str = Field(max_length=150)
    family_name_scientific: str = None
    family_name_english: str = None
    family_name_german: str = None
    species_name_scientific: str = None
    species_name_english: str = None
    species_name_german: str = None
    class Config:
        orm_mode = True


class Bird(BirdBase):
    occurrences: List[Occurrence] = Field(default=[], readOnly=True, nullable=False)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }

class FileResponse(BaseModel):
    file_url: str

    class Config:
        orm_mode = True


pictureResponse = {
    200: {
        "content":
            {
                "image/jpeg":
                    {
                        "schema":
                            {
                                "type": "string",
                                "format": "binary"
                            }
                    }
            },
        "description": "Return the picture.",
    }
}

User.update_forward_refs()
UserBase.update_forward_refs()
Occurrence.update_forward_refs()
Bird.update_forward_refs()
BirdBase.update_forward_refs()
