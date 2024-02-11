#!/usr/bin/python3
"""Unittest for BaseModel class"""
import unittest
import os
from models.base_model import BaseModel
import pep8


class TestBaseModel(unittest.TestCase):

    def test_pep8_BaseModel(self):
        pep_style = pep8.StyleGuide(quiet=True)
        peps = pep_style.check_files(['models/base_model.py'])
        self.assertEqual(peps.total_errors, 0, "Check pep8")

    def test_to_json(self):
        pass

    def test_save_BaseModel(self):
        self.base.save()
        self.assertNotEqual(self.base.created_at, self.base.updated_at)

    def setUp(self):
        self.testbasemodel = BaseModel()

    def test_kwarg(self):
        bm = BaseModel(name="base")
        self.assertEqual(type(bm).__name__, "BaseModel")
        self.assertFalse(hasattr(bm, "id"))
        self.assertFalse(hasattr(bm, "created_at"))
        self.assertTrue(hasattr(bm, "name"))
        self.assertFalse(hasattr(bm, "updated_at"))
        self.assertTrue(hasattr(bm, "__class__"))

    def test_doc(self):
        self.assertisNotNone(BaseModel.__doc__)


if __name__ == "__main__":
    unittest.main()
