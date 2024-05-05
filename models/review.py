#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Review(BaseModel, Base):
    """Represent a review.

    Attributes:
        place_id (str): The Place id.
        user_id (str): The User id.
        text (str): The text of the review.
    """

    __tablename__ = 'reviews'
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
