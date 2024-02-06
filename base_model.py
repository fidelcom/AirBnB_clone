#!/usr/bin/python3
import uuid
import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at

        if updated_at is None:
            self.updated_at = datetime.datetime.now()
        else:
            self.updated_at = updated_at

    def __str__(self):
        return ("[{}] ({}) ({})".format(self.__class__.__name__, self.id, self.__dict__))
    def save(self):
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy["created_at"] = dict_copy["created_at"].isoformat()
        dict_copy["updated_at"] = dict_copy["updated_at"].isoformat()
        return (dict_copy)
