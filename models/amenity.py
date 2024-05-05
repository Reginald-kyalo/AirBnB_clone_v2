#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """

    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False, overlaps="place_amenities")
