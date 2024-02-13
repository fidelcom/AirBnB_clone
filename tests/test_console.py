#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(cls):
        cls.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(""))
            cls.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(cls):
        h = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help quit"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_create(cls):
        h = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help create"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_EOF(cls):
        h = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help EOF"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_show(cls):
        h = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help show"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_destroy(cls):
        h = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help destroy"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_all(cls):
        h = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help all"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_count(cls):
        h = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help count"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help_update(cls):
        h = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help update"))
            cls.assertEqual(h, output.getvalue().strip())

    def test_help(cls):
        h = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("help"))
            cls.assertEqual(h, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(cls):
        best_outcome = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_create_invalid_class(cls):
        best_outcome = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create MyModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_create_invalid_syntax(cls):
        best_outcome = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        best_outcome = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_create_object(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "User.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "State.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "City.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "Amenity.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "Place.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
            cls.assertLess(0, len(output.getvalue().strip()))
            testKey = "Review.{}".format(output.getvalue().strip())
            cls.assertIn(testKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(cls):
        best_outcome = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(".show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_invalid_class(cls):
        best_outcome = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show MyModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_missing_id_space_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show User"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show State"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show City"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Amenity"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Place"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Review"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_missing_id_dot_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.show()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show User 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show State 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show City 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Place 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("show Review 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_show_objects_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "show BaseModel {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "show User {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "show State {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "show Place {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "show City {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "show Amenity {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "show Review {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.show({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_missing_class(cls):
        best_outcome = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(".destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_invalid_class(cls):
        best_outcome = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy User"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy State"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy City"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Place"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Review"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_id_missing_dot_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_invalid_id_space_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_destroy_objects_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "destroy BaseModel {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "show User {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "show State {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "show Place {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "show City {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "show Amenity {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "show Review {}".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.destroy({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.destory({})".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(command))
            cls.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalid_class(cls):
        best_outcome = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all MyModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_all_objects_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all"))
            cls.assertIn("BaseModel", output.getvalue().strip())
            cls.assertIn("User", output.getvalue().strip())
            cls.assertIn("State", output.getvalue().strip())
            cls.assertIn("Place", output.getvalue().strip())
            cls.assertIn("City", output.getvalue().strip())
            cls.assertIn("Amenity", output.getvalue().strip())
            cls.assertIn("Review", output.getvalue().strip())

    def test_all_objects_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(".all()"))
            cls.assertIn("BaseModel", output.getvalue().strip())
            cls.assertIn("User", output.getvalue().strip())
            cls.assertIn("State", output.getvalue().strip())
            cls.assertIn("Place", output.getvalue().strip())
            cls.assertIn("City", output.getvalue().strip())
            cls.assertIn("Amenity", output.getvalue().strip())
            cls.assertIn("Review", output.getvalue().strip())

    def test_all_single_object_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            cls.assertIn("BaseModel", output.getvalue().strip())
            cls.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all User"))
            cls.assertIn("User", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all State"))
            cls.assertIn("State", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all City"))
            cls.assertIn("City", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all Amenity"))
            cls.assertIn("Amenity", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all Place"))
            cls.assertIn("Place", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("all Review"))
            cls.assertIn("Review", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_single_object_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            cls.assertIn("BaseModel", output.getvalue().strip())
            cls.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.all()"))
            cls.assertIn("User", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.all()"))
            cls.assertIn("State", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.all()"))
            cls.assertIn("City", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            cls.assertIn("Amenity", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.all()"))
            cls.assertIn("Place", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.all()"))
            cls.assertIn("Review", output.getvalue().strip())
            cls.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missing_class(cls):
        best_outcome = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(".update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_invalid_class(cls):
        best_outcome = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update MyModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_id_space_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update User"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update State"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update City"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Amenity"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Place"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Review"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_id_dot_notation(cls):
        best_outcome = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.update()"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_invalid_id_space_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update User 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update State 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update City 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Place 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("update Review 1"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_invalid_id_dot_notation(cls):
        best_outcome = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(cls):
        best_outcome = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
            test_cmd = "update BaseModel {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
            test_cmd = "update User {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
            test_cmd = "update State {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
            test_cmd = "update City {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
            test_cmd = "update Amenity {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
            test_cmd = "update Place {}".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(cls):
        best_outcome = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
            test_cmd = "BaseModel.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
            test_cmd = "User.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
            test_cmd = "State.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
            test_cmd = "City.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
            test_cmd = "Amenity.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
            test_cmd = "Place.update({})".format(test_id)
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(cls):
        best_outcome = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update BaseModel {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update User {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update State {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update City {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update Amenity {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update Place {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "update Review {} attr_name".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(cls):
        best_outcome = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "BaseModel.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "User.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "State.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "City.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "Amenity.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "Place.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            test_cmd = "Review.update({}, attr_name)".format(test_id)
            cls.assertFalse(HBNBCommand().onecmd(test_cmd))
            cls.assertEqual(best_outcome, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_id = output.getvalue().strip()
        test_cmd = "update BaseModel {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["BaseModel.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_id = output.getvalue().strip()
        test_cmd = "update User {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["User.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_id = output.getvalue().strip()
        test_cmd = "update State {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["State.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_id = output.getvalue().strip()
        test_cmd = "update City {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["City.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_id = output.getvalue().strip()
        test_cmd = "update Amenity {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Amenity.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_id = output.getvalue().strip()
        test_cmd = "update Review {} attr_name 'attr_value'".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Review.{}".format(test_id)].__dict__
        cls.assertTrue("attr_value", test_dictionary["attr_name"])

    def test_update_valid_string_attr_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            t_id = output.getvalue().strip()
        test_cmd = "BaseModel.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["BaseModel.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            t_id = output.getvalue().strip()
        test_cmd = "User.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["User.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            t_id = output.getvalue().strip()
        test_cmd = "State.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["State.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            t_id = output.getvalue().strip()
        test_cmd = "City.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["City.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            t_id = output.getvalue().strip()
        test_cmd = "Place.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            t_id = output.getvalue().strip()
        test_cmd = "Amenity.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Amenity.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            t_id = output.getvalue().strip()
        test_cmd = "Review.update({}, attr_name, 'attr_value')".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Review.{}".format(t_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

    def test_update_valid_int_attr_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} max_guest 98".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(98, test_dictionary["max_guest"])

    def test_update_valid_int_attr_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            t_id = output.getvalue().strip()
        test_cmd = "Place.update({}, max_guest, 98)".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(t_id)].__dict__
        cls.assertEqual(98, test_dictionary["max_guest"])

    def test_update_valid_float_attr_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} latitude 7.2".format(test_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(7.2, test_dictionary["latitude"])

    def test_update_valid_float_attr_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            t_id = output.getvalue().strip()
        test_cmd = "Place.update({}, latitude, 7.2)".format(t_id)
        cls.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dictionary = storage.all()["Place.{}".format(t_id)].__dict__
        cls.assertEqual(7.2, test_dictionary["latitude"])

    def test_update_valid_dictionary_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_id = output.getvalue().strip()
        test_cmd = "update BaseModel {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["BaseModel.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_id = output.getvalue().strip()
        test_cmd = "update User {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["User.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_id = output.getvalue().strip()
        test_cmd = "update State {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["State.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_id = output.getvalue().strip()
        test_cmd = "update City {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["City.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_id = output.getvalue().strip()
        test_cmd = "update Amenity {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Amenity.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_id = output.getvalue().strip()
        test_cmd = "update Review {} ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Review.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

    def test_update_valid_dictionary_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            test_id = output.getvalue().strip()
        test_cmd = "BaseModel.update({}".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["BaseModel.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            test_id = output.getvalue().strip()
        test_cmd = "User.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["User.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            test_id = output.getvalue().strip()
        test_cmd = "State.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["State.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            test_id = output.getvalue().strip()
        test_cmd = "City.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["City.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "Place.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            test_id = output.getvalue().strip()
        test_cmd = "Amenity.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Amenity.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            test_id = output.getvalue().strip()
        test_cmd = "Review.update({}, ".format(test_id)
        test_cmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Review.{}".format(test_id)].__dict__
        cls.assertEqual("attr_value", test_dictionary["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} ".format(test_id)
        test_cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(98, test_dictionary["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "Place.update({}, ".format(test_id)
        test_cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(98, test_dictionary["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "update Place {} ".format(test_id)
        test_cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(9.8, test_dictionary["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            test_id = output.getvalue().strip()
        test_cmd = "Place.update({}, ".format(test_id)
        test_cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmd)
        test_dictionary = storage.all()["Place.{}".format(test_id)].__dict__
        cls.assertEqual(9.8, test_dictionary["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            cls.assertEqual("0", output.getvalue().strip())

    def test_count_object(cls):
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("User.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("State.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Place.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("City.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            cls.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            cls.assertFalse(HBNBCommand().onecmd("Review.count()"))
            cls.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
