#!/usr/bin/python3
"""User entity implementation."""

import re

import uuid

from app import bcrypt, db

from app.models.base_model import BaseModel

from sqlalchemy.orm import validates

class User(BaseModel):
    """Represents a platform user."""

    __tablename__ = 'users'

    # for the table
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, password=None, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        # Initialize password field
        self.password = ""
        # If a password is provided during initialization, hash it immediately
        if password:
            self.hash_password(password)
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    # validating functions
    @validates('first_name', 'last_name')
    def _validate_name(self, field_name, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        if len(value.strip()) > 50:
            raise ValueError(f"{field_name} must be at most 50 characters")
        return value.strip()

    @validates('email')
    def _validate_email(self, field_name, value): 
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email must be a non-empty string")
        email = value.strip()
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            raise ValueError("email must be a valid email address")
        return email
    
    @validates('is_admin')
    def validate_is_admin(self, field_name, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        return value