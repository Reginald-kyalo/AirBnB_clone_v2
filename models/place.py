#!/usr/bin/python3
"""Defines the Place class."""
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """Represent a place.

    Attributes:
        city_id (str): The City id.
        user_id (str): The User id.
        name (str): The name of the place.
        description (str): The description of the place.
        number_rooms (int): The number of rooms of the place.
        number_bathrooms (int): The number of bathrooms of the place.
        max_guest (int): The maximum number of guests of the place.
        price_by_night (int): The price by night of the place.
        latitude (float): The latitude of the place.
        longitude (float): The longitude of the place.
        amenity_ids (list): A list of Amenity ids.
    """

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', ForeignKey('places.id'),
                                 primary_key=True),
                          Column('amenity_id', ForeignKey('amenities.id'),
                                 primary_key=True)
                          )
    __tablename__ = 'places'
    city_id = Column(String(36), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False, overlaps="place_amenities")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            reviews_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
