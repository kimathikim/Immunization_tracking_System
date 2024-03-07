#!/usr/bin/python3
"""Define class fro the vaccine model """
# import models
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Vaccine_administration(BaseModel, Base):
    __tablename__ = 'vaccine_administration'
    administration_date = Column(DateTime)
    confirmation_status = Column(String(20))
    practitioner_name = Column(String(60) ,nullable=True)
    child_id = Column(String(60), ForeignKey('children.id'))
    vaccine_id = Column(String(60), ForeignKey('vaccine.id'))
    practitioner_id = Column(String(60), ForeignKey('health_practitioner.id'))

    child = relationship("Child", back_populates="vaccine_administrations")
    vaccine = relationship("Vaccine", back_populates="vaccine_administrations")
    practitioner = relationship("Practitioner")


    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the vaccine class"""
        super().__init__(*args, **kwargs)
