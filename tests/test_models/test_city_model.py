#!/usr/bin/python3

"""
    city model test.
"""

import unittest
from models.base_model import BaseModel
from models.city import City


class TestUser(unittest.TestCase):

    def test_type_name(self):
        set_city = City()
        name = getattr(set_city, "name")
        self.assertIsInstance(name, str)

    def test_City_inheritance(self):
        set_city = City()
        self.assertIsInstance(set_city, BaseModel)

    def test_User_attributes(self):
        set_city = City()
        self.assertTrue("state_id" in set_city.__dir__())
        self.assertTrue("name" in set_city.__dir__())


