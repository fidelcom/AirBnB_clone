#!/usr/bin/python3
import models
from uuid import uuid4
from datetime import datetime

"""
Module BaseModel
Parent of all classes
"""


class BaseModel:
    """Base class for Airbnb clone project
        Methods:
            __init__(self, *args, **kwargs)
            __str__(self)
            __save(self)
            __repr__(self)
            to_dict(self)
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize attributes: random uuid, dates created/updated
        """
        dform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, dform)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """
        Update instance with updated time & save to serialized file
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Return dic with string formats of times; add class info to dic
        """
        dict_copy = self.__dict__.copy()
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        dict_copy["__class__"] = self.__class__.__name__
        return dict_copy

    def __str__(self):
        """
        Return string of info about model
        """
        name = self.__class__.__name__
        return "[{}] ({}) {}".format(name, self.id, self.__dict__)
