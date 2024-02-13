#!/usr/bin/python3
"""Unittest for BaseModel class"""
import unittest
import os
from models.base_model import BaseModel
import pep8


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def test_pep8_BaseModel(self):
        """Doc"""
        pep_style = pep8.StyleGuide(quiet=True)
        peps = pep_style.check_files(['models/base_model.py'])
        self.assertEqual(peps.total_errors, 0, "Check pep8")

    def test_to_json(self):
        """Doc"""
        pass

    def test_save_BaseModel(self):
        """Doc"""
        base = BaseModel()
        base.save()
        self.assertIsNotNone(base.updated_at)
        self.assertNotEqual(base.created_at, base.updated_at)

    def setUp(self):
        """Doc"""
        self.test_base_model = BaseModel()

    def test_kwarg(self):
        """Doc"""
        bm = BaseModel(name="base")
        self.assertEqual(type(bm).__name__, "BaseModel")
        self.assertTrue(hasattr(bm, "id"))
        self.assertTrue(hasattr(bm, "created_at"))
        self.assertTrue(hasattr(bm, "name"))
        self.assertTrue(hasattr(bm, "updated_at"))
        self.assertTrue(hasattr(bm, "__class__"))

    def test_doc(self):
        """Doc"""
        self.assertIsNotNone(BaseModel.__doc__)


if __name__ == "__main__":
    unittest.main()
