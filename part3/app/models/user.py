#!/usr/bin/python3
"""User entity implementation."""

import re
import uuid
from app.models.base_model import BaseModel
from app import bcrypt,db
from .base_model import BaseModel  # Import BaseModel from its module


class User(BaseModel):
    """Represents a platform user."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self._first_name = ""
        self._last_name = ""
        self._email = ""
        self._is_admin = False
        # Initialize password field
        self.password = ""

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        # If a password is provided during initialization, hash it immediately
        if password:
            self.hash_password(password)

    # ... (Keep existing validation methods and properties unchanged) ...

    # --- New methods for Task-1 ---

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

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
