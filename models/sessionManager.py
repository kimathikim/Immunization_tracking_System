#!/usr/bin/python3
"""Define class for session management"""
# import models
from datetime import datetime, timedelta
from models.base_model import Base, BaseModel
from sqlalchemy import INT, Column, String, DateTime


# from sqlalchemy.orm import relationship
class Session(BaseModel, Base):
    """Representation of the Session class"""

    __tablename__ = "session"
    email = Column(String(60), nullable=False)
    expiration_time = Column(DateTime, nullable=False
                             ,default=datetime.utcnow() + timedelta(minutes=30))
    
    def __init__(self, *args, **kwargs):
        """initialize a combination of the
        BaseModel and the practitioner class"""
        super().__init__(*args, **kwargs)
