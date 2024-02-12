#!/usr/bin/python3
"""Unnittest module for State"""
import unittest
import os
import pep8
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test cases for State"""

    @classmethod
    def setUpClass(self):
        """Doc"""
        self.set_state = State()
        self.set_state.name = "Lagos_AKA_THE_BEST_STATE"

    @classmethod
    def tearDownClass(self):
        """Doc"""
        del self.set_state
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        pep_style = pep8.StyleGuide(quiet=True)
        peps = pep_style.check_files(['models/state.py'])
        self.assertEqual(peps.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        """Doc"""
        self.assertTrue(issubclass(self.set_state.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        """Doc"""
        self.assertIsNotNone(State.__doc__)

    def test_has_attributes(self):
        """Doc"""
        self.assertTrue('id' in self.set_state.__dict__)
        self.assertTrue('created_at' in self.set_state.__dict__)
        self.assertTrue('updated_at' in self.set_state.__dict__)
        self.assertTrue('name' in self.set_state.__dict__)

    def test_attributes_are_strings(self):
        """Doc"""
        self.assertEqual(type(self.set_state.name), str)

    def test_save(self):
        """Doc"""
        self.set_state.save()
        self.assertNotEqual(self.set_state.created_at,
                            self.set_state.updated_at)

    def test_to_dict(self):
        """Doc"""
        self.assertEqual('to_dict' in dir(self.set_state), True)


if __name__ == "__main__":
    unittest.main()
