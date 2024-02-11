#!/usr/bin/python3s
"""
    place model test
"""

import unittest
from models.base_model import BaseModel
from models.place import Place


class TestUser(unittest.TestCase):

    def setUp(self):
        self.set_place = Place()

    def TearDown(self):
        pass

    def test_Place_inheritance(self):

        self.assertIsInstance(self.set_place, BaseModel)

    def test_Place_attributes(self):
        self.assertTrue("city_id" in self.set_place.__dir__())
        self.assertTrue("user_id" in self.set_place.__dir__())
        self.assertTrue("description" in self.set_place.__dir__())
        self.assertTrue("name" in self.set_place.__dir__())
        self.assertTrue("number_rooms" in self.set_place.__dir__())
        self.assertTrue("max_guest" in self.set_place.__dir__())
        self.assertTrue("price_by_night" in self.set_place.__dir__())
        self.assertTrue("latitude" in self.set_place.__dir__())
        self.assertTrue("longitude" in self.set_place.__dir__())
        self.assertTrue("amenity_ids" in self.set_place.__dir__())

    def test_type_amenity(self):
        amenity = getattr(self.set_place, "amenity_ids")
        self.assertIsInstance(amenity, list)

    def test_type_longitude(self):
        longitude = getattr(self.set_place, "longitude")
        self.assertIsInstance(longitude, float)

    def test_type_latitude(self):
        latitude = getattr(self.set_place, "latitude")
        self.assertIsInstance(latitude, float)

    def test_type_price_by_night(self):
        price_by_night = getattr(self.set_place, "price_by_night")
        self.assertIsInstance(price_by_night, int)

    def test_type_max_guest(self):
        max_guest = getattr(self.set_place, "max_guest")
        self.assertIsInstance(max_guest, int)

    def test_type_number_bathrooms(self):
        number_bathrooms = getattr(self.set_place, "number_bathrooms")
        self.assertIsInstance(number_bathrooms, int)

    def test_type_number_rooms(self):
        number_rooms = getattr(self.set_place, "number_rooms")
        self.assertIsInstance(number_rooms, int)

    def test_type_description(self):
        description = getattr(self.set_place, "description")
        self.assertIsInstance(description, str)

    def test_type_name(self):
        name = getattr(self.set_place, "name")
        self.assertIsInstance(name, str)

    def test_type_user_id(self):
        user_id = getattr(self.set_place, "user_id")
        self.assertIsInstance(user_id, str)

    def test_type_city_id(self):
        city_id = getattr(self.set_place, "city_id")
        self.assertIsInstance(city_id, str)
