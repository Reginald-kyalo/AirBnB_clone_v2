#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Sets up attributes and methods for storage
    for serializing and deserializing hbnb instances

    Returns:
        file_path (str): path to json file
        objects (dict): dictionary of instances to serialize into json
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns dictionary of available instances"""
        a_dict = {}
        if cls is not None:
            for k, v in FileStorage.__objects.items():
                if isinstance(v, cls):
                    a_dict[k] = v
            return a_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Saves created instances to objects and sets custom key"""
        my_key = type(obj).__name__ + '.' + str(obj.id)
        FileStorage.__objects[my_key] = obj

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            for k, v in FileStorage.__objects.items():
                if v is obj:
                    del FileStorage.__objects[k]
                    break

    def save(self):
        """Serializes objects to json file"""
        obj = FileStorage.__objects
        with open(FileStorage.__file_path, "w") as json_file:
            objdict = {key: value.to_dict() for key, value in obj.items()}
            json.dump(objdict, json_file, indent=4)

    def reload(self):
        """Deserializes json file to objects dictionary"""
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as json_file:
                objdict = json.load(json_file)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    cls = globals()[cls_name]
                    self.new(cls(**o))
        else:
            pass
