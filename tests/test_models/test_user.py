#!/usr/bin/python3
"""Unittest for User"""
import unittest
import os
import pep8
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Test cases for class User"""
    @classmethod
    def setUpClass(self):
        """Doc"""
        self.set_user = User()
        self.set_user.first_name = "Airbnb"
        self.set_user.last_name = "User"
        self.set_user.email = "airbnb@mail.com"
        self.set_user.password = "root"

    @classmethod
    def tearDownClass(self):
        """Doc"""
        del self.set_user
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        pep_style = pep8.StyleGuide(quiet=True)
        peps = pep_style.check_files(['models/user.py'])
        self.assertEqual(peps.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        """Doc"""
        self.assertTrue(issubclass(self.set_user.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        """Doc"""
        self.assertIsNotNone(User.__doc__)

    def test_has_attributes(self):
        """Doc"""
        self.assertTrue('email' in self.set_user.__dict__)
        self.assertTrue('id' in self.set_user.__dict__)
        self.assertTrue('created_at' in self.set_user.__dict__)
        self.assertTrue('updated_at' in self.set_user.__dict__)
        self.assertTrue('password' in self.set_user.__dict__)
        self.assertTrue('first_name' in self.set_user.__dict__)
        self.assertTrue('last_name' in self.set_user.__dict__)

    def test_attributes_are_strings(self):
        """Doc"""
        self.assertEqual(type(self.set_user.email), str)
        self.assertEqual(type(self.set_user.password), str)
        self.assertEqual(type(self.set_user.first_name), str)
        self.assertEqual(type(self.set_user.first_name), str)

    def test_save(self):
        """Doc"""
        self.set_user.save()
        self.assertNotEqual(self.set_user.created_at, self.set_user.updated_at)

    def test_to_dict(self):
        """Doc"""
        self.assertEqual('to_dict' in dir(self.set_user), True)


if __name__ == "__main__":
    unittest.main()
