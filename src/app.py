# Asumiendo que esto está en tu archivo models.py

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    firstname = Column(String(250), nullable=True)
    lastname = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    
    def to_dict(self):
        return {
            "ID": self.ID,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }

class Planet(Base):
    __tablename__ = 'planet'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))

    def to_dict(self):
        return {"ID": self.ID, "name": self.name, "description": self.description}

class Character(Base):
    __tablename__ = 'character'
    ID = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))

    def to_dict(self):
        return {"ID": self.ID, "name": self.name, "description": self.description}

# Continuar con las relaciones y la tabla asociativa...
