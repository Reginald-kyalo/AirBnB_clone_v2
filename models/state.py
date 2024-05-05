#!/usr/bin/python3
"""Defines the State class."""
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """Represent a state.

    Attributes:
        name (str): The name of the state.
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="delete", backref="state")

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def cities(self):
            """Get list of cities associated with current state"""
            cities_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
