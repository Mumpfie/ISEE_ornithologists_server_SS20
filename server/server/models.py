from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship

from .database import Base
from .queryClasses import Color, Size, Shape, Breeding


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)
    picture_url = Column(String(100))
    bird_occurrences = relationship('Occurrence', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Occurrence(Base):
    __tablename__ = "Occurrence"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    note = Column(Text)
    picture_url = Column(String(100))
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Float)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    bird_id = Column(Integer, ForeignKey('bird.id'), nullable=False)

    def __repr__(self):
        return '<Occurrence {} {} {}>'.format(self.id, self.timestamp, self.user_id)


class Bird(Base):
    __tablename__ = "bird"

    id = Column(Integer, primary_key=True)
    taxon = Column(String(25))
    genus = Column(String(25))
    order = Column(String(25))
    family_scientific_name = Column(String(25), ForeignKey('family.name_scientific'), nullable=False)
    species_scientific_name = Column(String(25), ForeignKey('species.name_scientific'), nullable=False)
    authority = Column(String(40))
    color = Column(Enum(Color))
    size = Column(Enum(Size))
    shape = Column(Enum(Shape))
    breeding = Column(Enum(Breeding))
    subregion = Column(String(150))
    picture_url = Column(String(100))
    bird_occurrences = relationship('Occurrence', backref='bird')

    def __repr__(self):
        return '<Bird {}>'.format(self.species_scientific_name)


class Family(Base):
    __tablename__ = "family"

    name_scientific = Column(String(25), primary_key=True)
    name_english = Column(String(50))
    name_german = Column(String(50))
    birds = relationship('Bird', backref='family')

    def __repr__(self):
        return '<Family {}>'.format(self.name_scientific)


class Species(Base):
    __tablename__ = "species"

    name_scientific = Column(String(25), primary_key=True)
    name_english = Column(String(50))
    name_german = Column(String(50))
    birds = relationship('Bird', backref='species')

    def __repr__(self):
        return '<Species {}>'.format(self.name_scientific)
