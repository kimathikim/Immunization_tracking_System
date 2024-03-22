#!/usr/bin/python3
"""Define class for hospital"""
# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String, column
from sqlalchemy.orm import relationship


# from sqlalchemy.orm import relationship
class Hospital(BaseModel, Base):
    """Representation of the parent class"""
    __tablename__ = "hospital"
    name = Column(String(60), nullable=False)
    location = Column(String(60), nullable=False)
    practitioner = relationship()
    
    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the practitioner class"""
        super().__init__(*args, **kwargs)
