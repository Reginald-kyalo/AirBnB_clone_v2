#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represent a User.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    __tablename__ = 'users'
    email = Column(String(128), nullable=True)
    password = Column(String(128), nullable=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    places = relationship("Place", backref="user", cascade="delete",
                          primaryjoin="User.id == Place.user_id")
    reviews = relationship("Review", backref="user", cascade="delete")
