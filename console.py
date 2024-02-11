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


class HBNBCommand(cmd.Cmd):
    """
    Entry to command interpreter
    """
    prompt = "(hbnb) "
    __is__classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
            }

    def do_quit(self, arg):
        """Exit on quit"""
        return True

    def do_EOF(self, arg):
        """Exit on Ctrl-D"""
        print("")
        return True

    def emptyline(self):
        """Overwrite default behavior to repeat last cmd"""
        pass

    def do_create(self, arg):
        """
        Create instance specified by user
        """
        arg_lex = parse(arg)
        if len(arg_lex) == 0:
            print("** class name missing **")
        elif arg_lex[0] not in HBNBCommand.__is__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_lex[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Print string representation: name and id
        """
        arg_lex = parse(arg)
        obj_dict = storage.all()
        if len(arg_lex) == 0:
            print("** class name missing **")
        elif arg_lex[0] not in HBNBCommand.__is__classes:
            print("** class doesn't exist **")
        elif len(arg_lex) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lex[0], arg_lex[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_lex[0], arg_lex[1])])

    def do_destroy(self, arg):
        """
        Destroy instance specified by user; Save changes to JSON file
        """
        arg_lex = parse(arg)
        obj_dict = storage.all()
        if len(arg_lex) == 0:
            print("** class name missing **")
        elif arg_lex[0] not in HBNBCommand.__is__classes:
            print("** class doesn't exist **")
        elif len(arg_lex) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lex[0], arg_lex[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_lex[0], arg_lex[1])]
            storage.save()

    def do_all(self, arg):
        """
        Print all objects or all objects of specified class
        """
        arg_lex = parse(arg)
        if len(arg_lex) > 0 and arg_lex[0] not in HBNBCommand.__is__classes:
            print("** class doesn't exist **")
        else:
            obj_lex = []
            for obj in storage.all().values():
                if len(arg_lex) > 0 and arg_lex[0] == obj.__class__.__name__:
                    obj_lex.append(obj.__str__())
                elif len(arg_lex) == 0:
                    obj_lex.append(obj.__str__())
            print(obj_lex)

    def do_update(self, arg):
        """
        Update if given exact object, exact attribute
        """
        arg_lex = parse(arg)
        obj_dict = storage.all()

        if len(arg_lex) == 0:
            print("** class name missing **")
            return False
        if arg_lex[0] not in HBNBCommand.__is__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_lex) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_lex[0], arg_lex[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_lex) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_lex) == 3:
            try:
                type(eval(arg_lex[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_lex) == 4:
            obj = obj_dict["{}.{}".format(arg_lex[0], arg_lex[1])]
            if arg_lex[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_lex[2]])
                obj.__dict__[arg_lex[2]] = valtype(arg_lex[3])
            else:
                obj.__dict__[arg_lex[2]] = arg_lex[3]
        elif type(eval(arg_lex[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_lex[0], arg_lex[1])]
            for k, v in eval(arg_lex[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """
        Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        arg_lex = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_lex[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def default(self, arg):
        """
        Accepts class name followed by arguement
        """
        arg_dictionary = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_lex = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_lex[1])
            if match is not None:
                command = [arg_lex[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dictionary.keys():
                    call = "{} {}".format(arg_lex[0], command[1])
                    return arg_dictionary[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
