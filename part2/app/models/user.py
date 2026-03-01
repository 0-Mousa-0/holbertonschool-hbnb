#!/usr/bin/python3
"""User entity implementation."""

import re

from app.models.base_model import BaseModel


class User(BaseModel):
    """Represents a platform user."""

    def __init__(self, first_name, last_name, email, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self._first_name = ""
        self._last_name = ""
        self._email = ""
        self._is_admin = False

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @staticmethod
    def _validate_name(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        if len(value.strip()) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value.strip()

    @staticmethod
    def _validate_email(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email must be a non-empty string")
        email = value.strip()
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            raise ValueError("email must be a valid email address")
        return email

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_name(value, "first_name")
        self.save()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_name(value, "last_name")
        self.save()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)
        self.save()

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self._is_admin = value
        self.save()
