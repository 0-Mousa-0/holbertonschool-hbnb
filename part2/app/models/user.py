#!/usr/bin/python3
from datetime import datetime
import uuid


class User:
    def __init__(self, id , firstName , lastName , admin,  email, password , createDate , updateDate):
        self.id = str(uuid.uuid4())
        self.firstName = self._validate_string(firstName, "First Name")
        self.lastName = self._validate_string(lastName, "Last Name")
        self._admin = bool(admin)
        self.email = email
        self.__password = password
        self.createDate = datetime.now()
        self.updateDate = datetime.now()

    def _validate_string(self, value, field_name):
            if not value or not isinstance(value, str):
                raise ValueError(f"{field_name} must be a non-empty string")
            return value

    def profileUpdate(self, firstName=None, lastName=None, email=None):
        if firstName: self.firstName = firstName
        if lastName: self.lastName = lastName
        if email: self.email = email
        self.updateDate = datetime.now()

    def verify_password(self, password):
        return self.__password == password


