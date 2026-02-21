#!/usr/bin/python3
import uuid
from datetime import datetime

class Amenity:
    def __init__(self, id = str(uuid.uuid4()) , name = "", **kwargs):
        self.id = id
        self.name = self.verify_name(name)
        self.createDate = kwargs.get("createDate", datetime.now())
        self.updateDate = kwargs.get("updateDate", datetime.now())

    def verify_name(self, name):
        if not isinstance(name, str):
            raise TypeError('name must be a string')
        if not name or len(name) > 50:
            raise ValueError('name must be between 50 characters')
        return name

    def update(self, data):
        if 'name' in data:
            self.name = self.verify_name(data['name'])
        self.updateDate = datetime.now()
        return self.updateDate , self.name