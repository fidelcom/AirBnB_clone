#!/usr/bin/python3
"""
Unittest to test FileStorage class
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """testing file storage"""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        basemodel = BaseModel()
        users = User()
        states = State()
        places = Place()
        cities = City()
        amenities = Amenity()
        reviews = Review()
        models.storage.new(basemodel)
        models.storage.new(users)
        models.storage.new(states)
        models.storage.new(places)
        models.storage.new(cities)
        models.storage.new(amenities)
        models.storage.new(reviews)
        self.assertIn("BaseModel." + basemodel.id, models.storage.all().keys())
        self.assertIn(basemodel, models.storage.all().values())
        self.assertIn("User." + users.id, models.storage.all().keys())
        self.assertIn(users, models.storage.all().values())
        self.assertIn("State." + states.id, models.storage.all().keys())
        self.assertIn(states, models.storage.all().values())
        self.assertIn("Place." + places.id, models.storage.all().keys())
        self.assertIn(places, models.storage.all().values())
        self.assertIn("City." + cities.id, models.storage.all().keys())
        self.assertIn(cities, models.storage.all().values())
        self.assertIn("Amenity." + amenities.id, models.storage.all().keys())
        self.assertIn(amenities, models.storage.all().values())
        self.assertIn("Review." + reviews.id, models.storage.all().keys())
        self.assertIn(reviews, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        basemodel = BaseModel()
        users = User()
        states = State()
        places = Place()
        cities = City()
        amenities = Amenity()
        reviews = Review()
        models.storage.new(basemodel)
        models.storage.new(users)
        models.storage.new(states)
        models.storage.new(places)
        models.storage.new(cities)
        models.storage.new(amenities)
        models.storage.new(reviews)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + basemodel.id, save_text)
            self.assertIn("User." + users.id, save_text)
            self.assertIn("State." + states.id, save_text)
            self.assertIn("Place." + places.id, save_text)
            self.assertIn("City." + cities.id, save_text)
            self.assertIn("Amenity." + amenities.id, save_text)
            self.assertIn("Review." + reviews.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        basemodel = BaseModel()
        users = User()
        states = State()
        places = Place()
        cities = City()
        amenities = Amenity()
        reviews = Review()
        models.storage.new(basemodel)
        models.storage.new(users)
        models.storage.new(states)
        models.storage.new(places)
        models.storage.new(cities)
        models.storage.new(amenities)
        models.storage.new(reviews)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + basemodel.id, objs)
        self.assertIn("User." + users.id, objs)
        self.assertIn("State." + states.id, objs)
        self.assertIn("Place." + places.id, objs)
        self.assertIn("City." + cities.id, objs)
        self.assertIn("Amenity." + amenities.id, objs)
        self.assertIn("Review." + reviews.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
