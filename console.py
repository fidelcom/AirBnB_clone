#!/usr/bin/python3
"""Entry to command interpreter"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    c_braces = re.search(r"\{(.*?)\}", arg)
    brac = re.search(r"\[(.*?)\]", arg)
    if c_braces is None:
        if brac is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lex = split(arg[:brac.span()[0]])
            ret_lex = [i.strip(",") for i in lex]
            ret_lex.append(brac.group())
            return ret_lex
    else:
        lex = split(arg[:c_braces.span()[0]])
        ret_lex = [i.strip(",") for i in lex]
        ret_lex.append(c_braces.group())
        return ret_lex
