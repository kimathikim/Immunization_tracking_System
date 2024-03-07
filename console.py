#!/usr/bin/python3
"""ITS console"""
import cmd
import shlex
import models
from models.healthcare_provider import practitioner
from models.base_model import BaseModel

classes = {
    "Practitioner": practitioner,
}


class ITSCommand(cmd.Cmd):
    """ITS console"""

    prompt = "(ITS) "

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def empty_line(self):
        """Empty line + ENTER shouldn’t execute anything"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parse(self, args):
        """Create a dict from a list of strings in the form key=value"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0]
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """create a new insance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("Class name missing" "")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parse(args[1:])
            new_instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(new_instance)
        new_instance.save()

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("Class name missing" "")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split(arg)
        if len(args) == 0:
            print("Class name missing" "")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    del models.storage.all()[key]
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    # def do_update(self, arg):
    #     """Updates an instance based on the class name and id""


if __name__ == "__main__":
    ITSCommand().cmdloop()
