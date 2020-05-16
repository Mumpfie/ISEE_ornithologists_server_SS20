from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

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
    family_scientific_name = Column(String(25),
        ForeignKey('family.scientific_name'), nullable=False)
    species_scientific_name = Column(String(25),
        ForeignKey('species.scientific_name'), nullable=False)
    authority  = Column(String(25))
    color = Column(String(25))
    size = Column(String(25))
    shape = Column(String(25))
    breeding = Column(String(25))
    subregion = Column(String(25))
    picture_url = Column(String(100))
    bird_occurrences = relationship('Occurrence', backref='bird')

    def __repr__(self):
        return '<Bird {}>'.format(self.species_scientific_name)

class Family(Base):
    __tablename__ = "family"

    scientific_name = Column(String(25), primary_key=True)
    englisch_name = Column(String(25))
    german_name = Column(String(25))
    birds = relationship('Bird', backref='family')

    def __repr__(self):
        return '<Family {}>'.format(self.scientific_name)

class Species(Base):
    __tablename__ = "species"

    scientific_name = Column(String(25), primary_key=True)
    englisch_name = Column(String(25))
    german_name = Column(String(25))
    birds = relationship('Bird', backref='species')

    def __repr__(self):
        return '<Species {}>'.format(self.scientific_name)

