#!/usr/bin/python3
"""Define class fro the vaccine model """
# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String , ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel

class Disease(BaseModel, Base):
    """Representation of the parent class"""

    __tablename__ = "disease"
    disease = Column(String(60), nullable=False)
    disease_description = Column(String(1000), nullable=False)
    vaccine_id = Column(String(60), ForeignKey("vaccine.id"), nullable=False)
    

    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the vaccine class"""
        super().__init__(*args, **kwargs)
