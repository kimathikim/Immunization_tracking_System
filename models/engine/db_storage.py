#!/usr/bin/python3
"""This module defines a class to manage file storage
for immunization tracking system"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
import models
from models.healthcare_provider import Practitioner
from models.parent import Parent
from models.child import Child
from models.base_model import Base
from models.admin import Admin
from models.vaccineAdministration import Vaccine_administration
from models.vaccine import Vaccine
from models.diseases import Disease
from models.sessionManager import Session
from models.dueDate import Duedate

classes = {"Practitioner": Practitioner, "Parent": Parent, "Child": Child, "Admin": Admin, "Vaccine": Vaccine, "Vaccineadministration": Vaccine_administration, "Disease": Disease, "Session": Session, "Duedate": Duedate}




class DBStorage:
    """interacts with the MySQL database"""

    def __init__(self):
        """initializes the database storage engine"""
        IMS_MYSQL_USER = getenv("IMS_MYSQL_USER")
        IMS_MYSQL_PWD = getenv("IMS_MYSQL_PWD")
        IMS_MYSQL_HOST = getenv("IMS_MYSQL_HOST")
        IMS_MYSQL_DB = getenv("IMS_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                IMS_MYSQL_USER, IMS_MYSQL_PWD, IMS_MYSQL_HOST, IMS_MYSQL_DB
            ),
            pool_pre_ping=True,
        )
    # create a session factory
    

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database sesson"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieves an object w/class name and id
        """
        result = None
        try:
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                if obj.id == id:
                    result = obj
        except BaseException:
            pass
        return result

    def get_by_email(self, cls, email):
        """get a parent by email"""
        objs = self.__session.query(classes[cls]).all()
        for obj in objs:
            if obj.email == email:
                return obj
    def get_by_phone(self, cls, phone_no):
        """Get the user by their phone numbers"""
        objs = self.__session.query(classes[cls]).all()
        for obj in objs:
            if obj.phone_number == int(phone_no):
                return obj

    def get_by_token(self, cls, token):
        """get a parent by email"""
        objs = self.__session.query(classes[cls]).all()
        for obj in objs:
            if obj.reset_token == token:
                return obj

    def count(self, cls=None):
        """
        Counts number of objects in DBstorage
        """
        cls_counter = 0

        if cls is not None:
            objs = self.__session.query(classes[cls]).all()
            cls_counter = len(objs)
        else:
            for k, v in classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(classes[k]).all()
                    cls_counter += len(objs)
        return cls_counter
