#!/usr/bin/python3
"""Defines the class for the health practitioner"""

# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String, DateTime
from flask_login import UserMixin

# from sqlalchemy.orm import relationship


class Practitioner(UserMixin, BaseModel, Base):
    """Representation of health practitioner"""

    __tablename__ = "health_practitioner"
    profile_picture = Column(String(60), nullable=True)
    id_No = Column(String(60), nullable=True)
    first_name = Column(String(60), nullable=False)
    second_Name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(INT, nullable=True)
    password = Column(String(60), nullable=False)
    reset_token = Column(String(60), nullable=True)
 
    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel a e end the practitioner class"""
        super().__init__(*args, **kwargs)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.email)
