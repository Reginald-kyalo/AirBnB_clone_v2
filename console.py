#!/usr/bin/python3
"""Defines hbnb command intepreter"""
import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Sets up commands in command intepreter

    Args:
        prompt (str): prompt string stdout
        __classes (list): classes available
    """
    prompt = "(hbnb) "
    __classes = ['BaseModel',
                 'User',
                 'State',
                 'City',
                 'Place',
                 'Amenity',
                 'Review']

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """creates new instance of BaseModel
        saves it to JSON file
        prints the id
        Ex: (hbnb) create BaseModel
        """
        line = arg
        instance, args = line.split(' ', 1)
        if instance:
            if instance in HBNBCommand.__classes:
                new_instance = eval(instance)()
                print(new_instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

        if args:
            for item in args.split():
                if item:
                    split_item = item.split('=')
                if len(split_item) == 2:
                    k, v = split_item
                    v = v.strip('"').replace('_', ' ')
                    setattr(new_instance, k, v)
        new_instance.save()

    def do_show(self, arg):
        """prints string representation of instance
        based on class name
        Ex: (hbnb) show BaseModel
        """
        model_name = model_id = ""
        args = parse(arg)
        objs = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return
        else:
            model_name = args[0]
        if model_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        else:
            model_id = args[1]
        if "{}.{}".format(model_name, model_id) not in objs:
            print("** no instance found **")
            return
        else:
            print(objs["{}.{}".format(model_name, model_id)])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        save changes to JSON file
        """
        line = parse(arg)
        model_name = model_id = ""
        objs = storage.all()

        if len(line) >= 1:
            model_name = line[0]
        else:
            print("** class name missing **")
            return
        if model_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(line) >= 2:
            model_id = line[1]
        else:
            print("** instance id missing **")
            return
        if "{}.{}".format(model_name, model_id) not in objs:
            print("** no instance found **")
            return
        else:
            del objs["{}.{}".format(model_name, model_id)]
            storage.save()

    def do_all(self, arg):
        """prints all string representation of all instances
        based or not on the class name
        Ex: $ all BaseModel or $ all
        """
        args = parse(arg)
        objs = storage.all().values()
        list = []

        if args and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            for obj in objs:
                if args and args[0] == obj.__class__.__name__:
                    list.append(obj.__str__())
                elif not args:
                    list.append(obj.__str__())

            print(list)

    def do_update(self, arg):
        """adds or updates attribute to an instance
        saves changes to JSON file
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        model_name = model_id = attr_name = attr_val = ''
        args = parse(arg)
        objs = storage.all()

        if args:
            model_name = args[0]
        else:
            print("** class name missing **")
            return
        if model_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) >= 2:
            model_id = args[1]
        else:
            print("** instance id missing **")
            return
        if "{}.{}".format(model_name, model_id) not in objs.keys():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        my_obj = objs["{}.{}".format(model_name, model_id)]

        if len(args) == 4:
            attr_name = args[2]
            attr_val = args[3]
            if attr_name in my_obj.__class__.__dict__.keys():
                valtype = type(my_obj.__class__.dict__[attr_name])
                my_obj.__dict__[attr_name] = valtype(attr_val.strip("\""))
            else:
                my_obj.__dict__[attr_name] = attr_val.strip("\"")
        elif type(eval(args[2])) == dict:
            for k, v in eval(args[2]).items():
                if (k in my_obj.__class__.__dict__.keys() and
                        type(my_obj.__class__.__dict__[k]) in
                        {str, int, float}):
                    valtype = type(my_obj.__class__.__dict__[k])
                    my_obj.__dict__[k] = valtype(v)
                else:
                    my_obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_EOF(self, line):
        """command to exit program"""
        return True

    def do_quit(self, line):
        """command to exit program"""
        return True

    def emptyline(self):
        """defaults to doing nothing if no command provided"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
