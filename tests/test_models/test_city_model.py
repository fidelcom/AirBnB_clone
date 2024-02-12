#!/usr/bin/python3

"""
    city model test.
"""

import unittest
from models.base_model import BaseModel
from models.city import City


class TestUser(unittest.TestCase):
    """Test cases for City class"""

    def test_type_name(self):
        """Doc"""
        set_city = City()
        name = getattr(set_city, "name")
        self.assertIsInstance(name, str)

    def test_City_inheritance(self):
        """Doc"""
        set_city = City()
        self.assertIsInstance(set_city, BaseModel)

    def test_User_attributes(self):
        """Doc"""
        set_city = City()
        self.assertTrue("state_id" in set_city.__dir__())
        self.assertTrue("name" in set_city.__dir__())


if __name__ == '__main__':
    unittest.main()
