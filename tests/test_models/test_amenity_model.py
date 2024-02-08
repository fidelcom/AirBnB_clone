#!/usr/bin/python3

"""
Amenity model test.
"""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):

    def test_Amenity_attribute_type(self):
        n_amenity = Amenity()
        n_value = getattr(n_amenity, "name")
        self.assertIsInstance(n_value, str)

    def test_Amenity_attributes(self):
        n_amenity = Amenity()
        self.assertTrue("name" in n_amenity.__dir__())

    def test_Amenity_inheritence(self):
        n_amenity = Amenity()
        self.assertIsInstance(n_amenity, BaseModel)


