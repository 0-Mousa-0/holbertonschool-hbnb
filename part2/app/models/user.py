#!/usr/bin/python3
import re
from datetime import datetime
import uuid


class User:
    # Class variable to track emails across ALL instances
    existing_emails = set()

    def __init__(self, firstName="", lastName="", admin=False, email="", **kwargs):
        # Generate ID inside __init__ so it's unique per instance
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.firstName = self.validate_string(firstName, "First Name")
        self.lastName = self.validate_string(lastName, "Last Name")
        self.admin = admin

        # Uniqueness check
        if email in User.existing_emails:
            raise ValueError("email already registered")

        self.email = self.verify_email(email)
        User.existing_emails.add(self.email)

        self.createDate = kwargs.get("createDate", datetime.now())
        self.updateDate = kwargs.get("updateDate", datetime.now())

    def validate_string(self, value, field_name):
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} must be a non-empty string")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be 50 characters maximum")
        return value

    def verify_email(self, email):
        if not isinstance(email, str) or not email:
            raise ValueError("email must be a non-empty string")
        if not re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$", email):
            raise ValueError("email must be a valid email address")
        return email

    def profileUpdate(self, data):
        # Use == for comparison
        if "firstName" in data:
            self.firstName = self.validate_string(data["firstName"], "First Name")
        if "lastName" in data:
            self.lastName = self.validate_string(data["lastName"], "Last Name")
        if "email" in data:
            new_email = data["email"]
            if new_email != self.email and new_email in User.existing_emails:
                raise ValueError("email already registered")
            # Update the global set
            User.existing_emails.discard(self.email)
            self.email = self.verify_email(new_email)
            User.existing_emails.add(self.email)
        if "admin" in data:
            self.admin = data["admin"]

        self.updateDate = datetime.now()