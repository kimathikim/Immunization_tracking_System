#!/usr/bin/python3
"""Define class fro the vaccine model """
# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel

class Vaccine(BaseModel, Base):
    """Representation of the parent class"""

    __tablename__ = "vaccine"
    names = Column(String(60), nullable=False)
    no_doses= Column(INT, nullable=False)
    disease = relationship("Disease", backref="vaccine")
    vaccine_administrations = relationship("Vaccine_administration", back_populates="vaccine")
    


    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the vaccine class"""
        super().__init__(*args, **kwargs)
