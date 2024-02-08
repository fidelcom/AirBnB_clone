#!/usr/bin/python3

import unittest
import os
import pep8
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.new_review = Review()
        self.new_review.place_id = "John"
        self.new_review.user_id = "Peter"
        self.new_review.text = "Excellent"

    @classmethod
    def tearDownClass(self):
        del self.new_review
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        pep_style = pep8.StyleGuide(quiet=True)
        peps = pep_style.check_files(['models/review.py'])
        self.assertEqual(peps.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        self.assertTrue(issubclass(self.new_review.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(Review.__doc__)

    def test_has_attributes(self):
        self.assertTrue('id' in self.new_review.__dict__)
        self.assertTrue('created_at' in self.new_review.__dict__)
        self.assertTrue('updated_at' in self.new_review.__dict__)
        self.assertTrue('place_id' in self.new_review.__dict__)
        self.assertTrue('text' in self.new_review.__dict__)
        self.assertTrue('user_id' in self.new_review.__dict__)

    def test_attributes_are_strings(self):
        self.assertEqual(type(self.new_review.text), str)
        self.assertEqual(type(self.new_review.place_id), str)
        self.assertEqual(type(self.new_review.user_id), str)

    def test_save(self):
        self.new_review.save()
        self.assertNotEqual(self.new_review.created_at, self.new_review.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.new_review), True)


if __name__ == "__main__":
    unittest.main()
