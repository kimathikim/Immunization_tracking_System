#!/usr/bin/python3
"""Defines the class for the health practitioner"""

# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String, DateTime

# from sqlalchemy.orm import relationship


class Admin(BaseModel, Base):
    """Representation of admin"""

    __tablename__ = "admin"
    first_name = Column(String(60), nullable=False)
    second_Name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(INT, nullable=False)
    password = Column(String(60), nullable=False)
    id_No = Column(String(60), nullable=False)
    reset_token = Column(String(60), nullable=True)
    profile_picture = Column(String(60), nullable=True)
    token_expiration = Column(DateTime, nullable=True)
    alternative_id = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel a e end the practitioner class"""
        super().__init__(*args, **kwargs)
