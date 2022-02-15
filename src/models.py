import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(12), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }

class Character(db.Model):
    # Here we define columns for the table character.
    # Notice that each column is also a normal Python instance attribute.
    character_id = Column(Integer, primary_key=True)
    character_homeworld = Column(String(250), nullable=False)
    character_name = Column(String(250))
    character_skill = Column(String(250), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.character_name

    def serialize(self):
        return {
            "character_id": self.character_id,
            "character_name": self.character_name,
        }


class Planet(db.Model):
    # Here we define columns for the table planet.
    # Notice that each column is also a normal Python instance attribute.
    planet_id = Column(Integer, primary_key=True)
    planet_population = Column(Integer, nullable=False)
    planet_diameter = Column(Integer, nullable=False)
    planet_climate = Column(String(250), nullable=False)
    planet_name = Column(String(250))

    def __repr__(self):
        return '<Planet %r>' % self.planet_name

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "planet_name": self.planet_name,
        }


class FavoriteCharacter(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    character_id = Column(Integer, ForeignKey('character.character_id'))

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    planet_id = Column(Integer, ForeignKey('planet.planet_id'))        

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

