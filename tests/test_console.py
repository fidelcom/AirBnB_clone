#!/usr/bin/python3
"""Defines unittests for console.py."""

import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand
"""from models.engine.file_strorage import FileStorage"""


class TestHBNBCommand(unittest.TestCase):
    @patch('console.storage.save')
    def test_create(self, mock_save):
        with patch('sys.stdout', new_callable=StringIO) as output:
            command = HBNBCommand()
            command.onecmd("create BaseModel")
            self.assertEqual(mock_save.call_count, 1)

    @patch('console.storage.all')
    def test_show(self, mock_all):
        mock_all.return_value = {"BaseModel.1234": "Some object"}
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            command = HBNBCommand()
            command.onecmd("show BaseModel 1234")
            self.assertEqual(mock_stdout.getvalue().strip(), "Some object")

    @patch('console.storage.all')
    @patch('console.storage.save')
    def test_destroy(self, mock_save, mock_all):
        mock_all.return_value = {"BaseModel.1234": "Some object"}
        command = HBNBCommand()
        command.onecmd("destroy BaseModel 1234")
        self.assertEqual(mock_all.return_value, {})
        self.assertEqual(mock_save.call_count, 1)

    @patch('console.storage.all')
    def test_all(self, mock_all):
        mock_all.return_value = {"BaseModel.1234": "Some object"}
        command = HBNBCommand()
        output = command.onecmd("all")
        self.assertEqual(output, None)

    def test_update_exact_object_excat_attribute(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            command = HBNBCommand()
            command.onecmd("update BaseModel 1234 name new_name")
            output = "** no instance found **"
            self.assertEqual(mock_stdout.getvalue().strip(), output)

    def test_update_missing_class_name(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            command = HBNBCommand()
            command.onecmd("update")
            output = "** class name missing **"
            self.assertEqual(mock_stdout.getvalue().strip(), output)

    @patch('console.storage.all')
    def test_count(self, mock_all):
        mock_all.return_value = {"BaseModel.1234": "Some object",
                                 "BaseModel.5678": "another object"}
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.command.onecmd("count BaseModel")
            self.assertEqual(mock_stdout.getvalue().strip(), "0")

    def setUp(self):
        self.command = HBNBCommand()

    def tearDown(self):
        pass

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_quit(self, mock_stdout):
        self.assertTrue(HBNBCommand().do_quit(""))
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_EOF(self, mock_stdout):
        self.assertTrue(self.command.do_EOF(""))
        self.assertEqual(mock_stdout.getvalue(), "\n")


if __name__ == '__main__':
    unittest.main()
