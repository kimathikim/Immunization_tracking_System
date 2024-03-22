#!/usr/bin/python3
"""Define class fro the childs parent"""
# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String
from sqlalchemy.orm import relationship


# from sqlalchemy.orm import relationship
class Parent(BaseModel, Base):
    """Representation of the parent class"""

    __tablename__ = "parent"
    first_name = Column(String(60), nullable=False)
    second_Name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone_number = Column(INT, nullable=False)
    password = Column(String(60), nullable=False)
    county = Column(String(60), nullable=False)
    children = relationship("Child", backref="parent" , cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the practitioner class"""
        super().__init__(*args, **kwargs)
