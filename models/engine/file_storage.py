#!/usr/bin/python3
"""
File Storage
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    serializes and deserialzes json files
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return dictionary of <class>.<id> : object instance
        """
        return self.__objects

    def new(self, obj):
        """
        Add new obj to existing dictionary of instances
        """
        class_name = obj.__class__.__name__
        self.__objects["{}.{}".format(class_name, obj.id)] = obj

    def save(self):
        """
        Save obj dictionaries to json file
        """
        dict_obj = self.__objects
        obj_dict = {obj: dict_obj[obj].to_dict() for obj in dict_obj.keys()}
        with open(self.__file_path, "w") as fp:
            json.dump(obj_dict, fp)

    def reload(self):
        """
        If json file exists, convert obj dicts back to instances
        """
        try:
            with open(self.__file_path) as fp:
                obj_dict = json.load(fp)
                for value in obj_dict.values():
                    class_name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(class_name)(**value))
        except FileNotFoundError:
            return

