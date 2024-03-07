#!/usr/bin/python3
"""will contain the base models that other classes will utilze"""
import models
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    id = Column(String(60), primary_key=True, nullable=False)
    Created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    Updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, **kwargs):
        """Initializing the BaseModel class"""
        if kwargs:
            """Set the attributes of the BaseModel class if not set"""
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("Created_at", None) and isinstance(kwargs["Created_at"], str):
                self.Created_at = datetime.strptime(kwargs["Created_at"], time)
            else:
                self.Created_at = datetime.utcnow()
            if kwargs.get("Updated_at", None) and isinstance(kwargs["Updated_at"], str):
                self.Updated_at = datetime.strptime(kwargs["Updated_at"], time)
            else:
                self.Updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.Created_at = datetime.utcnow()
            self.Updated_at = datetime.utcnow()

    def __str__(self):
        """Function used for representation of the baseModel class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self):
        """Function that converts the object att ributes and values intoa dictionary"""
        new_dict = self.__dict__.copy()
        if "Created_at" in new_dict:
            new_dict["Created_at"] = new_dict["Created_at"].strftime(time)
        if "Updated_at" in new_dict:
            new_dict["Updated_at"] = new_dict["Updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

    def save(self):
        """updates the public instance attribute with the current datetime"""
        self.Updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    # def delete(self):
    #     """Delete the current instance from the storage"""
    #    model.storage.delete(self)

    # genetate 
