#!/usr/bin/python3
"""Defines the City class."""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represent a city.

    Attributes:
        state_id (str): The state id.
        name (str): The name of the city.
    """

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(36), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
