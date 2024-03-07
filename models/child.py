#!/usr/bin/python3
"""Child class that inherits from BaseModel class and has parent_id attribute"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Child(BaseModel, Base):
    """Child class that inherits from BaseModel class and has parent_id attribute"""
    __tablename__ = 'children'
    first_name = Column(String(60), nullable=False)
    second_name = Column(String(60), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    parent_id = Column(String(60), ForeignKey('parent.id'), nullable=False)
    vaccine_administrations = relationship("Vaccine_administration", back_populates="child")
    
    
    def __init__(self, *args, **kwargs):
        """Initializes Child class"""
        super().__init__(*args, **kwargs)
