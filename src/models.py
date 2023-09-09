from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Tablas asociativas para las relaciones muchos-a-muchos
user_planet_association = Table('user_planet', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.ID')),
    Column('planet_id', Integer, ForeignKey('planet.ID'))
)

user_character_association = Table('user_character', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.ID')),
    Column('character_id', Integer, ForeignKey('character.ID'))
)

class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=True)
    lastname = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

    # Relaciones
    favorite_planets = relationship('Planet', secondary=user_planet_association, back_populates="users")
    favorite_characters = relationship('Character', secondary=user_character_association, back_populates="users")

    def to_dict(self):
        return {
            "ID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "favorite_planets": [planet.ID for planet in self.favorite_planets],
            "favorite_characters": [character.ID for character in self.favorite_characters]
        }

class Planet(Base):
    __tablename__ = 'planet'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))

    # Relaciones
    users = relationship('User', secondary=user_planet_association, back_populates="favorite_planets")

    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "description": self.description,
            "users": [user.ID for user in self.users]
        }

class Character(Base):
    __tablename__ = 'character'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))

    # Relaciones
    users = relationship('User', secondary=user_character_association, back_populates="favorite_characters")

    def to_dict(self):
        return {
            "ID": self.ID,
            "name": self.name,
            "description": self.description,
            "users": [user.ID for user in self.users]
        }
