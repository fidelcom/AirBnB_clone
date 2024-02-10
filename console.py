#!/usr/bin/python3
import cmd

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_EOF(self, line):
        return True

    def help_EOF(self):
        print('\n')

    def do_quit(self, line):
       return True

    def help_quit(self):
        print("Quit command to exit the program\n")

    def do_help(self, line):
        cmd.Cmd.do_help(self, line)

    def help_help(self):
        print('\n')

    def emptyline(self):
        pass

    def do_create(self, line):
        if not line:
            print("** class name missing **")
            return
	try:
            cls = eval(line)
        except NameError:
            print("** class doesn't exist **")
        instance = cls()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        if not line:
            print("** class name missing **")
        parts = line.split()
        try:
            cls = eval(parts[0])
        except NameError:
            print("** class doesn't exist **")
        if parts[1] is None:
            print("** instance id missing **")
        if not instance[cls][id]:
            print("* no instance found **")
        print(str(

if __name__ == '__main__':
    HBNBCommand().cmdloop()
