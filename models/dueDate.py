#!/usr/bin/python3
"""Define class for the due dates"""
# import models
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.vaccineAdministration import Vaccine_administration

class Duedate(BaseModel, Base):
    """This class define the table for the duedate"""
    __tablename__ = "vaccineDueDate"

    due_date = Column(String(60), nullable=False)
    vaccine_administration_id = Column(String(60), ForeignKey('vaccine_administration.id'), nullable=False)

    records = relationship("Vaccine_administration")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
